import requests
from flask import current_app

from app.models import ProcedureType
from app.scraper.other.config import PROCEDURE_TYPES_URL
from app.scraper.soup_parsing import safe_find_text, to_soup


def transform_procedure_type_xml_to_dict(soup):
    return {
        "lido_id": safe_find_text(soup, "Identifier"),
        "name": safe_find_text(soup, "Naam"),
    }


def procedure_type_exists(procedure_type_dict):
    institution = ProcedureType.query.filter(
        ProcedureType.name == procedure_type_dict.get("name")
    ).first()
    if institution:
        return True


def import_procedure_types_handler():
    r = requests.get(PROCEDURE_TYPES_URL)
    r.raise_for_status()

    procedure_types = to_soup(r.content).find_all("Proceduresoort")
    current_app.logger.info(f"Found {len(procedure_types)} procedure types")

    for procedure_type in procedure_types:
        procedure_type_dict = transform_procedure_type_xml_to_dict(procedure_type)

        if not procedure_type_exists(procedure_type_dict):
            ProcedureType.create(**procedure_type_dict)
            current_app.logger.info(
                f"New procedure type {procedure_type_dict.get('name')} added"
            )
