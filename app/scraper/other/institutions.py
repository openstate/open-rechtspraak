import requests
from flask import current_app

from app.models import Institution
from app.scraper.other.config import INSTITUTIONS_URL
from app.scraper.verdicts.soup_parsing import safe_find_text, to_soup


def transform_institution_xml_to_dict(soup):
    return {
        "lido_id": safe_find_text(soup, "Identifier"),
        "name": safe_find_text(soup, "Naam"),
        "abbrevation": safe_find_text(soup, "Afkorting") or None,
        "type": safe_find_text(soup, "Type"),
        "begin_date": safe_find_text(soup, "BeginDate") or None,
        "end_date": safe_find_text(soup, "EndDate") or None,
    }


def institution_exists(institution_dict):
    institution = Institution.query.filter(
        Institution.name == institution_dict.get("name")
    ).first()
    if institution:
        return True


def import_institutions_handler():
    r = requests.get(INSTITUTIONS_URL)
    r.raise_for_status()

    institutions = to_soup(r.content).find_all("Instantie")
    current_app.logger.info(f"Found {len(institutions)} institutions")

    for institution in institutions:
        institution_dict = transform_institution_xml_to_dict(institution)

        if not institution_exists(institution_dict):
            Institution.create(**institution_dict)
            current_app.logger.info(
                f"New institution {institution_dict.get('name')} added"
            )
