import json

from flask import current_app

from app.models import Person
from app.scraper.people.config import FAULTY_URL, SEARCH_ENDPOINT
from app.scraper.people.utils import search_strings
from app.scraper.rechtspraak_session import RechtspraakScrapeSession
from app.scraper.soup_parsing import extract_rnl_state, to_soup


def import_people_handler() -> None:
    with RechtspraakScrapeSession() as session:
        for search_string in search_strings():
            import_people_by_search_string(search_string, session)


def import_people_by_search_string(search_string: str, session: RechtspraakScrapeSession) -> None:
    current_app.logger.info(f"Importing people by search string '{search_string}' from {SEARCH_ENDPOINT}")
    """rnl-state"""

    query_params = {"searchterm": search_string}

    r = session.get(SEARCH_ENDPOINT, params=query_params, timeout=3)

    if not r.ok or r.url == FAULTY_URL:
        current_app.logger.error(
            f"Error during people collection: STATUS_CODE {r.status_code} | URL {r.url} | CONTENT {r.content}",
        )
        return

    try:
        soup = to_soup(r.content, features="html.parser")
        state = extract_rnl_state(soup).text
        people = json.loads(state).get("neroSearchResults")

        if len(people) == 0:
            current_app.logger.info(f"Found 0 people during people collection for search string '{search_string}'")
            return
    except json.JSONDecodeError:
        current_app.logger.exception(f"JSONDecodeError found when scraping {r.url}")
        return

    current_app.logger.debug(f"{len(people)} people found for search string '{search_string}'")

    for person in people:
        update_or_create_person(person)


def update_or_create_person(person: dict) -> Person:
    """This function ensures that a person is updated if one of their attributes is changed or gets created if they
    do not exist yet.
    """
    p_kwargs = Person.from_dict(person)
    return Person.update_or_create({"rechtspraak_id": p_kwargs.pop("rechtspraak_id")}, p_kwargs)
