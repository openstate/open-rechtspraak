from datetime import datetime, timedelta

from app.scraper.people.enrich_people import (
    RESCRAPE_AFTER_HOURS,
    enrich_people_handler,
    enrich_person,
    person_details_url,
)
from app.scraper.rechtspraak_session import RechtspraakScrapeSession
from app.tests.factories import PersonFactory


class TestEnrichPerson:
    def test_removed_at_is_not_set(self, requests_mock, person):
        requests_mock.get(person_details_url(person.rechtspraak_id), json={}, status_code=200)

        assert person.removed_from_rechtspraak_at is None
        with RechtspraakScrapeSession() as session:
            enrich_person(session, person)
        assert person.removed_from_rechtspraak_at is None

    def test_removed_at_is_set_on_http_error(self, requests_mock, person):
        requests_mock.get(person_details_url(person.rechtspraak_id), status_code=500)

        assert person.removed_from_rechtspraak_at is None
        with RechtspraakScrapeSession() as session:
            enrich_person(session, person)
        assert person.removed_from_rechtspraak_at is not None

    def test_removed_at_is_removed_on_successful_scrape(self, requests_mock):
        dt = datetime.now()
        person = PersonFactory(removed_from_rechtspraak_at=dt)
        requests_mock.get(person_details_url(person.rechtspraak_id), json={}, status_code=200)

        assert person.removed_from_rechtspraak_at == dt
        with RechtspraakScrapeSession() as session:
            enrich_person(session, person)
        assert person.removed_from_rechtspraak_at is None

    def test_should_scrape_if_never_scraped_before(self, requests_mock):
        person = PersonFactory(last_scraped_at=None)
        requests_mock.get(person_details_url(person.rechtspraak_id), json={}, status_code=200)

        assert person.last_scraped_at is None
        with RechtspraakScrapeSession() as session:
            enrich_person(session, person)
        assert person.last_scraped_at is not None


class TestEnrichPeopleHandler:
    def test_should_rescrape_if_scraped_n_hours_ago(self, requests_mock, freezer):
        long_time_ago = datetime(2020, 1, 1, 0, 0, 0)
        now = long_time_ago + timedelta(hours=RESCRAPE_AFTER_HOURS + 1)

        freezer.move_to(now)
        person = PersonFactory(last_scraped_at=long_time_ago)
        requests_mock.get(person_details_url(person.rechtspraak_id), json={}, status_code=200)

        assert person.last_scraped_at == long_time_ago
        enrich_people_handler()
        assert person.last_scraped_at == now

    def test_should_not_rescrape_if_too_early(self, requests_mock, freezer):
        long_time_ago = datetime(2020, 1, 1, 0, 0, 0)
        now = long_time_ago + timedelta(hours=RESCRAPE_AFTER_HOURS - 1)

        freezer.move_to(now)
        person = PersonFactory(last_scraped_at=long_time_ago)
        requests_mock.get(person_details_url(person.rechtspraak_id), json={}, status_code=200)

        assert person.last_scraped_at == long_time_ago
        enrich_people_handler()
        assert person.last_scraped_at == long_time_ago
