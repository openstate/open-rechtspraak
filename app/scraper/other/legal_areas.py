from typing import TYPE_CHECKING

from flask import current_app

from app.models import LegalArea
from app.scraper.other.config import LEGAL_AREAS_URL
from app.scraper.rechtspraak_session import RechtspraakScrapeSession
from app.scraper.soup_parsing import safe_find_text, to_soup

if TYPE_CHECKING:
    from bs4 import BeautifulSoup


def transform_legal_area_xml_to_dict(soup: BeautifulSoup) -> dict:
    return {
        "legal_area_lido_id": safe_find_text(soup, "Identifier"),
        "legal_area_name": safe_find_text(soup, "Naam"),
    }


def legal_area_exists(legal_area_dict: dict) -> bool:
    legal_area = LegalArea.query.filter(
        LegalArea.legal_area_lido_id == legal_area_dict.get("legal_area_lido_id"),
    ).first()

    return True if legal_area else False


def import_legal_areas_handler() -> None:
    with RechtspraakScrapeSession() as session:
        r = session.get(LEGAL_AREAS_URL)
        r.raise_for_status()

        main_areas = to_soup(r.content).find("Rechtsgebieden").find_all("Rechtsgebied", recursive=False)
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
                    current_app.logger.info(f"New legal area {legal_area_dict.get('legal_area_name')} added")
