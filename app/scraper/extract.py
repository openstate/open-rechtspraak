from datetime import datetime

import requests

from app.models import People, ProfessionalDetails
from app.scraper.config import DETAILS_ENDPOINT, HEADERS, SEARCH_ENDPOINT
from app.scraper.utils import (
    find_request_verification_token,
    format_payload,
    search_strings,
)


def import_people_handler():
    with requests.Session() as s:
        # We first need a CSRF token to be able to query the namenlijst.rechtspraak.nl API
        r = s.get("https://namenlijst.rechtspraak.nl/#!/zoeken/index")
        HEADERS["__RequestVerificationToken"] = find_request_verification_token(
            r.content
        )
        for search_string in search_strings():
            payload = format_payload(search_string)
            r = s.post(SEARCH_ENDPOINT, json=payload, headers=HEADERS)
            print(r.status_code, r.url, payload)

            if not r.ok:
                print("error", r.status_code, r.content)
                continue

            people = r.json().get("result", {}).get("model", {}).get("groupedItems", {})
            print(f"Found {len(people)} people.")
            for person in people:
                p_kwargs = People.from_dict(person)
                person_already_exists = People.query.filter(
                    People.toon_naam == p_kwargs.get("toon_naam")
                ).all()
                if not person_already_exists:
                    People.update_or_create(p_kwargs)


def enrich_people_handler():
    people = [People.query.first()]

    for person in people:
        r = requests.get(DETAILS_ENDPOINT + person.rechtspraak_id)
        print(r.status_code, r.url)

        if not r.ok:
            print("error", r.status_code, r.content)
            continue

        person_json = r.json().get("model", {})

        for beroepsgegeven in person_json.get("beroepsgegevens", []):
            pd_kwargs = ProfessionalDetails.transform_beroepsgegevens_dict(
                beroepsgegeven
            )
            ProfessionalDetails.create(**{"person_id": person.id, **pd_kwargs})

        for historisch_beroepsgegeven in person_json.get("historieBeroepsgegevens", []):
            pd_kwargs = ProfessionalDetails.transform_historisch_beroepsgegevens_dict(
                historisch_beroepsgegeven
            )
            ProfessionalDetails.create(**{"person_id": person.id, **pd_kwargs})

        person.last_scraped_at = datetime.now()
        person.save()
