import requests
from flask import current_app

from app.models import Institution
from app.scraper.soup_parsing import safe_find_text, to_soup


def transform_institution_xml_to_dict(soup):
    return {
        "lido_id": safe_find_text(soup, "identifier"),
        "name": safe_find_text(soup, "naam"),
        "abbrevation": safe_find_text(soup, "afkorting") or None,
        "type": safe_find_text(soup, "type"),
        "begin_date": safe_find_text(soup, "begindate") or None,
        "end_date": safe_find_text(soup, "enddate") or None,
    }


def institution_exists(institution_dict):
    institution = Institution.query.filter(
        Institution.name == institution_dict.get("name")
    ).first()
    if institution:
        return True


def import_institutions_handler():
    BASE_URL = "http://data.rechtspraak.nl/Waardelijst/Instanties"

    r = requests.get(BASE_URL)
    r.raise_for_status()

    institutions = to_soup(r.content).find_all("instantie")
    current_app.logger.info(f"Found {len(institutions)} institutions")

    for institution in institutions:
        institution_dict = transform_institution_xml_to_dict(institution)

        if not institution_exists(institution_dict):
            Institution.create(**institution_dict)
            current_app.logger.info(
                f"New institution {institution_dict.get('name')} added"
            )
