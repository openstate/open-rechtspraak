from datetime import datetime

import requests
from flask import current_app

from app.errors import EnrichError
from app.models import Verdict
from app.verdict_scraper.config import (
    DEFAULT_LIMIT,
    DEFAULT_SEARCH_QUERY_PARAMS,
    DETAILS_ENDPOINT,
    SEARCH_ENDPOINT,
)
from app.verdict_scraper.feed_parsing import extract_verdicts, safe_find_text, to_soup
from app.verdict_scraper.utils import verdict_already_exists


def import_verdicts_handler(start_datetime, end_datetime):
    # The search endpoint returns verdicts between two 'date' query params. If only one 'date' query param is given,
    # then only the verdicts of that date are returned.
    DEFAULT_SEARCH_QUERY_PARAMS["date"] = [start_datetime, end_datetime]

    while True:
        r = requests.get(SEARCH_ENDPOINT, params=DEFAULT_SEARCH_QUERY_PARAMS)
        current_app.logger.debug(f"Collecting verdicts from {r.url}")

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
            if not verdict_already_exists(verdict_kwargs):
                Verdict.create(**verdict_kwargs)
            else:
                current_app.logger.debug(
                    f'Verdict for {verdict_kwargs.get("ecli")} already exists'
                )

        DEFAULT_SEARCH_QUERY_PARAMS["from"] = (
            DEFAULT_SEARCH_QUERY_PARAMS["from"] + DEFAULT_LIMIT
        )


def enrich_verdicts_handler():
    # verdicts = Verdict.query.filter(Verdict.last_scraped_at.is_(None)).all()
    verdicts = Verdict.query.limit(1).all()
    for verdict in verdicts:
        try:
            enrich_verdict(verdict)
            find_people_for_verdict(verdict)
        except EnrichError:
            current_app.logger.error(
                "An unknown problem during verdict enrichment was encountered."
            )
            pass


def enrich_verdict(verdict):
    current_app.logger.debug(f"Enriching {verdict.ecli}")
    params = {"id": verdict.ecli}
    r = requests.get(DETAILS_ENDPOINT, params=params)
    current_app.logger.debug(f"Collecting verdict information from {r.url}")

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


def find_people_for_verdict(verdict):
    from sqlalchemy import func

    from app.models import Person

    people = Person.query.order_by(func.random()).limit(2).all()
    print(people)
    verdict.people = Person.query.order_by(func.random()).limit(2).all()
    verdict.save()
