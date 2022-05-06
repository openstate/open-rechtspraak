from datetime import datetime
from json import JSONDecodeError

import requests
from flask import current_app

from app.models import Person, ProfessionalDetail, SideJob
from app.people_scraper.config import DETAILS_ENDPOINT, HEADERS, SEARCH_ENDPOINT
from app.people_scraper.utils import (
    find_institution_for_professional_detail,
    find_request_verification_token,
    format_payload,
    professional_detail_already_exists,
    search_strings,
    side_job_already_exists,
)

FAULTY_URL = "https://mededeling.rechtspraak.nl/400"


def import_people_handler():
    with requests.Session() as s:
        # We first need a CSRF token to be able to query the namenlijst.rechtspraak.nl API
        r = s.get("https://namenlijst.rechtspraak.nl/#!/zoeken/index")
        HEADERS["__RequestVerificationToken"] = find_request_verification_token(
            r.content
        )
        current_app.logger.debug(
            f'Found CSRF token: {HEADERS["__RequestVerificationToken"]}'
        )

        for search_string in search_strings():
            payload = format_payload(search_string)
            r = s.post(SEARCH_ENDPOINT, json=payload, headers=HEADERS)

            current_app.logger.info(
                f"Collecting people from {r.url} with payload {payload}"
            )

            if not r.ok or r.url == FAULTY_URL:
                current_app.logger.error(
                    f"Error during people collection: STATUS_CODE {r.status_code} | URL {r.url} | CONTENT {r.content}"
                )
                continue

            try:
                people = (
                    r.json().get("result", {}).get("model", {}).get("groupedItems", {})
                )
            except JSONDecodeError:
                current_app.logger.error(f"JSONDecodeError found when scraping {r.url}")
                people = []

            current_app.logger.debug(f"{len(people)} people found for {r.url}")

            for person in people:
                p_kwargs = Person.from_dict(person)
                person_already_exists = Person.query.filter(
                    Person.toon_naam == p_kwargs.get("toon_naam")
                ).all()
                if not person_already_exists:
                    Person.create(**p_kwargs)
                else:
                    current_app.logger.debug(
                        f'Person with rechtspraak_id {p_kwargs.get("rechtspraak_id")} already exists'
                    )


def enrich_people_handler():
    people = Person.query.all()

    for person in people:
        enrich_person(person)


def person_details_url(rechtspraak_id: str) -> str:
    return DETAILS_ENDPOINT + rechtspraak_id


def enrich_person(person: Person) -> None:
    r = requests.get(person_details_url(person.rechtspraak_id))
    current_app.logger.info(
        f"Enriching person {person.id} with information from {r.url}"
    )

    if not r.ok or r.url == FAULTY_URL:
        current_app.logger.error(
            f"Error during enrichment of {person.id}: status {r.status_code}, url {r.url}"
        )
        person.removed_from_rechtspraak_at = datetime.now()
        person.last_scraped_at = datetime.now()
        person.save()
        return

    person_json = r.json().get("model", {})

    for beroepsgegeven in person_json.get("beroepsgegevens", []):
        pd_kwargs = ProfessionalDetail.transform_beroepsgegevens_dict(beroepsgegeven)
        if not professional_detail_already_exists(person, pd_kwargs):
            institution = find_institution_for_professional_detail(
                pd_kwargs.get("organisation")
            )
            ProfessionalDetail.create(
                **{"person_id": person.id, **pd_kwargs}, institution=institution
            )

    for historisch_beroepsgegeven in person_json.get("historieBeroepsgegevens", []):
        pd_kwargs = ProfessionalDetail.transform_historisch_beroepsgegevens_dict(
            historisch_beroepsgegeven
        )
        if not professional_detail_already_exists(person, pd_kwargs):
            institution = find_institution_for_professional_detail(
                pd_kwargs.get("organisation")
            )
            ProfessionalDetail.create(
                **{"person_id": person.id, **pd_kwargs}, institution=institution
            )

    for nevenbetrekking in person_json.get("huidigeNevenbetrekkingen", []):
        nb_kwargs = SideJob.transform_huidige_nevenbetrekkingen_dict(nevenbetrekking)
        if not side_job_already_exists(person, nb_kwargs):
            SideJob.create(**{"person_id": person.id, **nb_kwargs})

    for voorgaande_nevenbetrekking in person_json.get(
        "voorgaandeNevenbetrekkingen", []
    ):
        nb_kwargs = SideJob.transform_voorgaande_nevenbetrekkingen_dict(
            voorgaande_nevenbetrekking
        )
        if not side_job_already_exists(person, nb_kwargs):
            SideJob.create(**{"person_id": person.id, **nb_kwargs})

    person.removed_from_rechtspraak_at = None
    person.last_scraped_at = datetime.now()
    person.save()
