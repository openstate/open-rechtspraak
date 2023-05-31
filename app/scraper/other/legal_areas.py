import requests
from flask import current_app

from app.models import LegalArea
from app.scraper.other.config import LEGAL_AREAS_URL
from app.scraper.soup_parsing import safe_find_text, to_soup


def transform_legal_area_xml_to_dict(area):
    return {
        "legal_area_lido_id": safe_find_text(area, "Identifier"),
        "legal_area_name": safe_find_text(area, "Naam"),
    }


def legal_area_exists(legal_area_dict):
    legal_area = LegalArea.query.filter(
        LegalArea.legal_area_lido_id == legal_area_dict.get("legal_area_lido_id")
    ).first()
    if legal_area:
        return True


def import_legal_areas_handler():
    r = requests.get(LEGAL_AREAS_URL)
    r.raise_for_status()

    main_areas = (
        to_soup(r.content)
        .find("Rechtsgebieden")
        .findChildren("Rechtsgebied", recursive=False)
    )
    current_app.logger.info(f"Found {len(main_areas)} main legal areas")

    for main_area in main_areas:
        legal_area_dict = transform_legal_area_xml_to_dict(main_area)
        if not legal_area_exists(legal_area_dict):
            LegalArea.create(**legal_area_dict)

        sub_areas = main_area.find_all("Rechtsgebied")
        current_app.logger.info(f"Found {len(sub_areas)} sub areas")

        for sub_area in sub_areas:
            legal_area_dict = transform_legal_area_xml_to_dict(sub_area)

            if not legal_area_exists(legal_area_dict):
                LegalArea.create(**legal_area_dict)
                current_app.logger.info(
                    f"New legal area {legal_area_dict.get('legal_area_name')} added"
                )
