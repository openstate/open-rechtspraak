import os
from datetime import datetime

from flask import current_app
from setuptools import glob
from tqdm import tqdm

from app.models import Verdict
from app.scraper.verdicts.extract import (
    find_institution_for_verdict,
    find_legal_area_for_verdict,
    find_procedure_type_for_verdict,
)
from app.scraper.verdicts.soup_parsing import find_beslissing, safe_find_text, to_soup
from app.scraper.verdicts.utils import verdict_already_exists


def ecli_to_local_verdict_filename(ecli):
    return ecli.replace(":", "_") + ".xml"


def extract_verdict_details(soup, filepath):
    ecli = safe_find_text(soup, "dcterms:identifier")
    beslissings_text = find_beslissing(soup)
    verdict_kwargs = {
        "ecli": ecli,
        "uri": f"https://uitspraken.rechtspraak.nl/InzienDocument?id={ecli}",
        "issued": safe_find_text(soup, "dcterms:issued"),
        "zaak_nummer": safe_find_text(soup, "psi:zaaknummer"),
        "type": safe_find_text(soup, "dcterms:type"),
        "coverage": safe_find_text(soup, "dcterms:coverage"),
        "subject": safe_find_text(soup, "dcterms:subject"),
        "spatial": safe_find_text(soup, "dcterms:spatial"),
        "procedure": safe_find_text(soup, "psi:procedure"),
        "raw_xml": filepath,
        "last_scraped_at": datetime.now(),
        "contains_beslissing": True if beslissings_text else False,
        "beslissings_text": beslissings_text if beslissings_text else None,
    }
    return verdict_kwargs


def filepath_to_ecli(filepath):
    filename = os.path.basename(filepath)
    return filename[:-4].replace("_", ":")


def import_verdicts_from_files_handler():
    files = glob.glob("../open-rechtspraak-dataset/to_be_imported/**/*.xml")
    current_app.logger.info(f"Found {len(files)} verdicts in local files")

    for filepath in tqdm(files, mininterval=2):
        ecli = filepath_to_ecli(filepath)
        if not verdict_already_exists(ecli):
            soup = to_soup(open(filepath))
            verdict_kwargs = extract_verdict_details(soup, filepath)
            verdict = Verdict.create(**verdict_kwargs)

            find_institution_for_verdict(verdict, soup)
            find_procedure_type_for_verdict(verdict, soup)
            find_legal_area_for_verdict(verdict, soup)
