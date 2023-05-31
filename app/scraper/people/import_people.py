from json import JSONDecodeError

from flask import current_app

from app.models import Person
from app.scraper.people.config import FAULTY_URL, HEADERS, SEARCH_ENDPOINT
from app.scraper.people.utils import (
    find_request_verification_token,
    format_payload,
    search_strings,
)
from app.scraper.rechtspraak_session import RechtspraakScrapeSession


def import_people_handler():
    with RechtspraakScrapeSession() as session:
        # We first need a CSRF token to be able to query the namenlijst.rechtspraak.nl API
        r = session.get("https://namenlijst.rechtspraak.nl/#!/zoeken/index")
        HEADERS["__RequestVerificationToken"] = find_request_verification_token(
            r.content
        )
        current_app.logger.debug(
            f'Found CSRF token: {HEADERS["__RequestVerificationToken"]}'
        )

        for search_string in search_strings():
            import_people_by_search_string(search_string, session)


def import_people_by_search_string(
    search_string: str, session: RechtspraakScrapeSession
):
    payload = format_payload(search_string)
    current_app.logger.info(
        f"Importing people by search string '{search_string}' from {SEARCH_ENDPOINT}"
    )

    r = session.post(SEARCH_ENDPOINT, json=payload, headers=HEADERS, timeout=3)

    if not r.ok or r.url == FAULTY_URL:
        current_app.logger.error(
            f"Error during people collection: STATUS_CODE {r.status_code} | URL {r.url} | CONTENT {r.content}"
        )
        return

    try:
        people = r.json().get("result", {}).get("model", {}).get("groupedItems", {})
    except JSONDecodeError:
        current_app.logger.error(f"JSONDecodeError found when scraping {r.url}")
        people = []

    current_app.logger.debug(f"{len(people)} people found for {r.url}")

    for person in people:
        update_or_create_person(person)


def update_or_create_person(person: dict) -> Person:
    """
    This function ensures that a person is updated if one of their attributes is changed or gets created if they
    do not exist yet.
    """
    p_kwargs = Person.from_dict(person)
    return Person.update_or_create({"toon_naam": p_kwargs.pop("toon_naam")}, p_kwargs)
