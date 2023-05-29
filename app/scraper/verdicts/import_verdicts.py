import requests
from flask import current_app

from app.models import Verdict
from app.scraper.soup_parsing import extract_verdicts, to_soup
from app.scraper.verdicts.config import (
    DEFAULT_LIMIT,
    DEFAULT_SEARCH_QUERY_PARAMS,
    FAULTY_URL,
    SEARCH_ENDPOINT,
)
from app.scraper.verdicts.utils import verdict_already_exists


def import_verdicts_handler(start_datetime, end_datetime):
    # The search endpoint returns verdicts between two 'date' query params. If only one 'date' query param is given,
    # then only the verdicts of that date are returned.
    DEFAULT_SEARCH_QUERY_PARAMS["date"] = [start_datetime, end_datetime]

    while True:
        r = requests.get(SEARCH_ENDPOINT, params=DEFAULT_SEARCH_QUERY_PARAMS)
        current_app.logger.info(f"Collecting verdicts from {r.url}")

        if not r.ok or r.url == FAULTY_URL:
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
