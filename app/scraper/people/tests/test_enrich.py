from datetime import datetime

from app.scraper.people.extract import enrich_person, person_details_url
from app.tests.factories import PersonFactory


def test_removed_at_is_not_set(requests_mock):
    person = PersonFactory().save()
    requests_mock.get(
        person_details_url(person.rechtspraak_id), json={}, status_code=200
    )

    assert person.removed_from_rechtspraak_at is None
    enrich_person(person)
    assert person.removed_from_rechtspraak_at is None


def test_removed_at_is_set_on_http_error(requests_mock):
    person = PersonFactory().save()
    requests_mock.get(person_details_url(person.rechtspraak_id), status_code=500)

    assert person.removed_from_rechtspraak_at is None
    enrich_person(person)
    assert person.removed_from_rechtspraak_at is not None


def test_removed_at_is_removed_on_succesful_scrape(requests_mock):
    dt = datetime.now()
    person = PersonFactory(removed_from_rechtspraak_at=dt).save()
    requests_mock.get(
        person_details_url(person.rechtspraak_id), json={}, status_code=200
    )

    assert person.removed_from_rechtspraak_at is dt
    enrich_person(person)
    assert person.removed_from_rechtspraak_at is None
