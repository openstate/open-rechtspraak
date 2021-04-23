import math
from datetime import datetime

import requests
from flask import current_app

from app.errors import EnrichError
from app.models import Institution, LegalArea, PersonVerdict, ProcedureType, Verdict
from app.verdict_scraper.config import (
    DEFAULT_LIMIT,
    DEFAULT_SEARCH_QUERY_PARAMS,
    DETAILS_ENDPOINT,
    SEARCH_ENDPOINT,
)
from app.verdict_scraper.soup_parsing import (
    extract_verdicts,
    find_beslissing,
    find_institution_identifier,
    find_legal_area_identifier,
    find_procedure_type_identifier,
    safe_find_text,
    to_soup,
)
from app.verdict_scraper.utils import (
    person_verdict_already_exists,
    recognize_people,
    verdict_already_exists,
)


def import_verdicts_handler(start_datetime, end_datetime):
    # The search endpoint returns verdicts between two 'date' query params. If only one 'date' query param is given,
    # then only the verdicts of that date are returned.
    DEFAULT_SEARCH_QUERY_PARAMS["date"] = [start_datetime, end_datetime]

    while True:
        r = requests.get(SEARCH_ENDPOINT, params=DEFAULT_SEARCH_QUERY_PARAMS)
        current_app.logger.info(f"Collecting verdicts from {r.url}")

        if not r.ok or r.url == "https://mededeling.rechtspraak.nl/404":
            current_app.logger.error(
                f"Error during verdict collection: STATUS_CODE {r.status_code} | URL {r.url} | CONTENT {r.content}"
            )
            return

        verdicts = extract_verdicts(to_soup(r.content))

        if len(verdicts) == 0:
            current_app.logger.debug(f"No more verdicts found for {r.url}")
            break
        else:
            current_app.logger.debug(f"{len(verdicts)} verdicts found for {r.url}")

        for verdict in verdicts:
            verdict_kwargs = {
                "ecli": verdict.id.text,
                "title": verdict.title.text,
                "summary": verdict.summary.text,
                "uri": verdict.link["href"],
            }
            if not verdict_already_exists(verdict_kwargs.get("ecli")):
                Verdict.create(**verdict_kwargs)
            else:
                current_app.logger.debug(
                    f'Verdict for {verdict_kwargs.get("ecli")} already exists'
                )

        DEFAULT_SEARCH_QUERY_PARAMS["from"] = (
            DEFAULT_SEARCH_QUERY_PARAMS["from"] + DEFAULT_LIMIT
        )


def enrich_verdicts_handler():
    base_query = Verdict.query.filter(Verdict.last_scraped_at.is_(None))
    total_no_of_verdicts = base_query.count()
    runs = math.ceil(total_no_of_verdicts / 1000)
    current_app.logger.info(
        f"{runs} number of runs needed to enrich {total_no_of_verdicts} un-enriched verdicts"
    )

    for run in range(0, runs):
        offset = run * 1000
        current_app.logger.info(f"Run {run} with offset {offset}")
        verdicts = base_query.limit(1000).all()
        for verdict in verdicts:
            try:
                if verdict.raw_xml is None:
                    enrich_verdict(verdict)

                if verdict.raw_xml is not None:
                    find_people_for_verdict(verdict)
                    find_institution_for_verdict(verdict)
                    find_procedure_type_for_verdict(verdict)
                    find_legal_area_for_verdict(verdict)
            except EnrichError:
                current_app.logger.error(
                    "An unknown problem during verdict enrichment was encountered."
                )
                pass


def enrich_verdict(verdict):
    current_app.logger.debug(f"Enriching {verdict.ecli}")
    params = {"id": verdict.ecli}
    r = requests.get(DETAILS_ENDPOINT, params=params)
    current_app.logger.info(f"Collecting verdict information from {r.url}")

    if not r.ok or r.url == "https://mededeling.rechtspraak.nl/404":
        current_app.logger.error(
            f"Error during verdict enrichment: {verdict.id}, {verdict.ecli}, {r.status_code}, {r.url}"
        )
        return

    soup = to_soup(r.content)
    verdict.deeplink = safe_find_text(soup, "dcterms:identifier")
    verdict.issued = safe_find_text(soup, "dcterms:issued")
    verdict.zaak_nummer = safe_find_text(soup, "psi:zaaknummer")
    verdict.type = safe_find_text(soup, "dcterms:type")
    verdict.coverage = safe_find_text(soup, "dcterms:coverage")
    verdict.subject = safe_find_text(soup, "dcterms:subject")
    verdict.spatial = safe_find_text(soup, "dcterms:spatial")
    verdict.procedure = safe_find_text(soup, "psi:procedure")
    verdict.raw_xml = str(soup)
    verdict.last_scraped_at = datetime.now()
    verdict.save()


def find_people_for_verdict(verdict, people=None, soup=None):
    current_app.logger.debug(
        f"Starting with people finding for verdict {verdict.ecli} ({verdict.id})"
    )

    if not soup:
        soup = to_soup(verdict.raw_xml)
    beslissing = find_beslissing(soup)

    if not beslissing:
        current_app.logger.debug(
            f"No beslissing found in verdict {verdict.ecli} ({verdict.id})"
        )
        return

    verdict.contains_beslissing = True
    verdict.save()

    related_people = recognize_people(beslissing, people)
    current_app.logger.debug(
        f"Found {len(related_people)} related people in verdict {verdict.ecli} ({verdict.id})"
    )

    for person in related_people:
        pv = {"role": "rechter", "verdict_id": verdict.id, "person_id": person.id}

        if not person_verdict_already_exists(pv):
            PersonVerdict.create(**pv)
        else:
            current_app.logger.debug(
                f"PersonVerdict for person {person.id} and verdict {verdict.id} already exists"
            )


def find_institution_for_verdict(verdict, soup=None):
    if not soup:
        soup = to_soup(verdict.raw_xml)
    institution_identifier = find_institution_identifier(soup)

    if not institution_identifier:
        return

    institution = Institution.query.filter(
        Institution.lido_id.ilike(institution_identifier)
    ).first()
    if institution:
        verdict.institution = institution
        verdict.save()
        current_app.logger.debug(
            f"Institution {institution.name} matched with and verdict {verdict.id} ({verdict.ecli})"
        )
    else:
        current_app.logger.warning(
            f"No institution found for verdict {verdict.id} ({verdict.ecli})"
        )


def find_procedure_type_for_verdict(verdict, soup=None):
    if not soup:
        soup = to_soup(verdict.raw_xml)
    procedure_type_identifier = find_procedure_type_identifier(soup)

    if not procedure_type_identifier:
        current_app.logger.debug(
            f"No procedure type found in xml from verdict {verdict.id} ({verdict.ecli})"
        )
        return

    procedure_type = ProcedureType.query.filter(
        ProcedureType.lido_id.ilike(procedure_type_identifier)
    ).first()
    if procedure_type:
        verdict.procedure_type = procedure_type
        verdict.save()
        current_app.logger.debug(
            f"Procedure type {procedure_type.name} matched with and verdict {verdict.id} ({verdict.ecli})"
        )
    else:
        current_app.logger.warning(
            f"No procedure type found for verdict {verdict.id} ({verdict.ecli})"
        )


def find_legal_area_for_verdict(verdict, soup=None):
    if not soup:
        soup = to_soup(verdict.raw_xml)

    legal_area_identifier = find_legal_area_identifier(soup)

    if not legal_area_identifier:
        current_app.logger.debug(
            f"No legal area found in xml from verdict {verdict.id} ({verdict.ecli})"
        )
        return

    legal_area = LegalArea.query.filter(
        LegalArea.legal_area_lido_id.ilike(legal_area_identifier)
    ).first()
    if legal_area:
        verdict.legal_area = legal_area
        verdict.save()
        current_app.logger.debug(
            f"Legal area {legal_area.legal_area_name} matched with and verdict {verdict.id} ({verdict.ecli})"
        )
    else:
        current_app.logger.warning(
            f"No legal area found for verdict {verdict.id} ({verdict.ecli})"
        )
