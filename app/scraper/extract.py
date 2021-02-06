import requests

from app.models import People
from app.scraper.config import HEADERS, SEARCH_ENDPOINT
from app.scraper.utils import format_payload, search_strings


def collect_and_save_people():
    with requests.Session() as s:
        for search_string in search_strings():
            payload = format_payload(search_string)
            r = s.post(SEARCH_ENDPOINT, json=payload, headers=HEADERS)
            print(r.url, payload)

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
