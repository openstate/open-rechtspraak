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


def import_verdicts_handler(start_datetime: str, end_datetime: str):
    """
    Datetime parameters must be formatted as such: %Y-%m-%dT%H:%M:%S

    See https://www.rechtspraak.nl/Uitspraken/paginas/open-data.aspx for more details on how the search endpoint works.
    """

    params = DEFAULT_SEARCH_QUERY_PARAMS
    params["date"] = [start_datetime, end_datetime]

    while True:
        current_app.logger.info(
            f"Collecting verdicts from {SEARCH_ENDPOINT} with params: {params}"
        )
        r = requests.get(SEARCH_ENDPOINT, params=params)

        if not r.ok or r.url == FAULTY_URL:
            current_app.logger.error(
                f"Error during verdict collection: STATUS_CODE {r.status_code} | URL {r.url} | CONTENT {r.content}"
            )
            return

        verdicts = extract_verdicts(to_soup(r.content))

        current_app.logger.info(f"{len(verdicts)} verdicts found for {r.url}")

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

        params["from"] = params["from"] + DEFAULT_LIMIT

        if len(verdicts) < DEFAULT_LIMIT:
            current_app.logger.info(
                f"Last scrape yielded less than {DEFAULT_LIMIT}, indicating no more verdicts can be found."
            )
            break
