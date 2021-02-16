from datetime import datetime

import requests
from flask import current_app

from app.models import People, ProfessionalDetails, SideJobs
from app.people_scraper.config import DETAILS_ENDPOINT, HEADERS, SEARCH_ENDPOINT
from app.people_scraper.utils import (
    find_request_verification_token,
    format_payload,
    professional_detail_already_exists,
    search_strings,
    side_job_already_exists,
)


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

            current_app.logger.debug(
                f"Collecting people from {r.url} with payload {payload}"
            )

            if not r.ok:
                current_app.logger.error(
                    f"Error during people collection: STATUS_CODE {r.status_code} | URL {r.url} | CONTENT {r.content}"
                )
                continue

            people = r.json().get("result", {}).get("model", {}).get("groupedItems", {})

            current_app.logger.debug(f"{len(people)} people found for {r.url}")

            for person in people:
                p_kwargs = People.from_dict(person)
                person_already_exists = People.query.filter(
                    People.toon_naam == p_kwargs.get("toon_naam")
                ).all()
                if not person_already_exists:
                    People.create(**p_kwargs)
                else:
                    current_app.logger.debug(
                        f'Person with rechtspraak_id {p_kwargs.get("rechtspraak_id")} already exists'
                    )


def enrich_people_handler():
    people = People.query.all()

    for person in people:
        r = requests.get(DETAILS_ENDPOINT + person.rechtspraak_id)
        current_app.logger.debug(
            f"Enriching person {person.id} with information from {r.url}"
        )

        if not r.ok:
            current_app.logger.error(
                f"Error during person enrichment: {person.id}, {r.status_code}, {r.url}, {r.content}"
            )
            continue

        person_json = r.json().get("model", {})

        for beroepsgegeven in person_json.get("beroepsgegevens", []):
            pd_kwargs = ProfessionalDetails.transform_beroepsgegevens_dict(
                beroepsgegeven
            )
            if not professional_detail_already_exists(person, pd_kwargs):
                ProfessionalDetails.create(**{"person_id": person.id, **pd_kwargs})

        for historisch_beroepsgegeven in person_json.get("historieBeroepsgegevens", []):
            pd_kwargs = ProfessionalDetails.transform_historisch_beroepsgegevens_dict(
                historisch_beroepsgegeven
            )
            if not professional_detail_already_exists(person, pd_kwargs):
                ProfessionalDetails.create(**{"person_id": person.id, **pd_kwargs})

        for nevenbetrekking in person_json.get("huidigeNevenbetrekkingen", []):
            nb_kwargs = SideJobs.transform_huidige_nevenbetrekkingen_dict(
                nevenbetrekking
            )
            if not side_job_already_exists(person, nb_kwargs):
                SideJobs.create(**{"person_id": person.id, **nb_kwargs})

        for voorgaande_nevenbetrekking in person_json.get(
            "voorgaandeNevenbetrekkingen", []
        ):
            nb_kwargs = SideJobs.transform_voorgaande_nevenbetrekkingen_dict(
                voorgaande_nevenbetrekking
            )
            if not side_job_already_exists(person, nb_kwargs):
                SideJobs.create(**{"person_id": person.id, **nb_kwargs})

        person.last_scraped_at = datetime.now()
        person.save()
