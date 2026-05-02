from datetime import datetime, timedelta
from typing import ClassVar

from app.models import ProfessionalDetail
from app.scraper.people.enrich_people import (
    RESCRAPE_AFTER_HOURS,
    enrich_people_handler,
    enrich_person,
    person_details_url,
)
from app.scraper.rechtspraak_session import RechtspraakScrapeSession
from app.tests.factories import PersonFactory


class TestEnrichPerson:
    rechtspraak_response: ClassVar = {
        "completeDateTime": "/Date(1777637082369+0200)/",
        "errorMessage": None,
        "model": {
            "achternaam": "Test",
            "beroepsgegevens": [],
            "beroepsgegevensBuitenRM": [],
            "geenOpgaveNevenbetrekkingen": False,
            "historieBeroepsgegevens": [],
            "huidigeNevenbetrekkingen": [],
            "status": "Gepubliceerd",
            "toonNaam": "mw. mr. drs. A.B. Test",
            "vervultGeenNevenbetrekkingen": True,
            "voorgaandeBetrekkingen": [],
            "voorgaandeNevenbetrekkingen": [],
        },
        "status": 1,
        "validationMessages": None,
    }

    def test_removed_at_is_not_set(self, requests_mock, person):
        requests_mock.get(person_details_url(person.rechtspraak_id), json=self.rechtspraak_response, status_code=200)

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
        requests_mock.get(person_details_url(person.rechtspraak_id), json=self.rechtspraak_response, status_code=200)

        assert person.removed_from_rechtspraak_at == dt
        with RechtspraakScrapeSession() as session:
            enrich_person(session, person)
        assert person.removed_from_rechtspraak_at is None

    def test_removed_at_is_set_if_empty_model_returned(self, requests_mock):
        person = PersonFactory()
        response = {
            "completeDateTime": "/Date(1777636689856+0200)/",
            "errorMessage": None,
            "model": None,
            "status": 1,
            "validationMessages": None,
        }
        requests_mock.get(person_details_url(person.rechtspraak_id), json=response, status_code=200)

        assert person.removed_from_rechtspraak_at is None
        with RechtspraakScrapeSession() as session:
            enrich_person(session, person)
        assert person.removed_from_rechtspraak_at

    def test_should_scrape_if_never_scraped_before(self, requests_mock):
        person = PersonFactory(last_scraped_at=None)
        requests_mock.get(person_details_url(person.rechtspraak_id), json={}, status_code=200)

        assert person.last_scraped_at is None
        with RechtspraakScrapeSession() as session:
            enrich_person(session, person)
        assert person.last_scraped_at is not None


class TestEnrichPersonProfessionalDetails:
    def test_no_professional_details_are_created_if_none_exist(self, requests_mock):
        person = PersonFactory()
        response = {
            "completeDateTime": "/Date(1777637082369+0200)/",
            "errorMessage": None,
            "model": {
                "achternaam": "Test",
                "beroepsgegevens": [],
                "toonNaam": "mw. mr. drs. A.B. Test",
            },
            "status": 1,
            "validationMessages": None,
        }
        requests_mock.get(person_details_url(person.rechtspraak_id), json=response, status_code=200)

        assert person.professional_detail == []
        with RechtspraakScrapeSession() as session:
            enrich_person(session, person)
        assert person.professional_detail == []

    def test_current_professional_detail_is_created_if_exist(self, requests_mock):
        person = PersonFactory()
        pd = {
            "begindatum": "/Date(1769900400000+0100)/",
            "functieOmschrijving": "Rechter-plaatsvervanger",
            "hoofdfunctie": True,
            "instantieOmschrijving": "Rechtbank Amsterdam",
            "opmerkingen": "test",
        }
        response = {
            "completeDateTime": "/Date(1777637082369+0200)/",
            "errorMessage": None,
            "model": {
                "achternaam": "Test",
                "beroepsgegevens": [pd],
                "toonNaam": "mw. mr. drs. A.B. Test",
            },
            "status": 1,
            "validationMessages": None,
        }
        requests_mock.get(person_details_url(person.rechtspraak_id), json=response, status_code=200)

        assert person.professional_detail == []
        assert len(ProfessionalDetail.query.all()) == 0

        with RechtspraakScrapeSession() as session:
            enrich_person(session, person)

        assert len(person.professional_detail) == 1
        assert len(ProfessionalDetail.query.all()) == 1

        assert person.professional_detail[0].function == pd.get("functieOmschrijving")
        assert person.professional_detail[0].start_date == datetime(2026, 2, 1, 0, 0)
        assert person.professional_detail[0].main_job is True
        assert person.professional_detail[0].remarks == pd.get("opmerkingen")
        assert person.professional_detail[0].organisation == pd.get("instantieOmschrijving")
        assert person.professional_detail[0].outside_of_judiciary is False

    def test_historical_professional_detail_is_created_if_exist(self, requests_mock):
        person = PersonFactory()
        pd = {
            "begindatum": "/Date(1769900400000+0100)/",
            "einddatum": "/Date(1869900400000+0100)/",
            "functie": "Rechter-plaatsvervanger",
            "instantie": "Rechtbank Amsterdam",
        }
        response = {
            "completeDateTime": "/Date(1777637082369+0200)/",
            "errorMessage": None,
            "model": {
                "achternaam": "Test",
                "historieBeroepsgegevens": [pd],
                "toonNaam": "mw. mr. drs. A.B. Test",
            },
            "status": 1,
            "validationMessages": None,
        }
        requests_mock.get(person_details_url(person.rechtspraak_id), json=response, status_code=200)

        assert person.professional_detail == []
        assert len(ProfessionalDetail.query.all()) == 0

        with RechtspraakScrapeSession() as session:
            enrich_person(session, person)

        assert len(person.professional_detail) == 1
        assert len(ProfessionalDetail.query.all()) == 1

        assert person.professional_detail[0].function == pd.get("functie")
        assert person.professional_detail[0].start_date == datetime(2026, 2, 1, 0, 0)
        assert person.professional_detail[0].end_date == datetime(2029, 4, 3, 10, 46, 40)
        assert person.professional_detail[0].remarks == pd.get("opmerkingen")
        assert person.professional_detail[0].organisation == pd.get("instantie")
        assert person.professional_detail[0].outside_of_judiciary is False

    def test_professional_detail_outside_of_judiciary_is_created_if_exist(self, requests_mock):
        person = PersonFactory()
        pd = {
            "begindatum": "/Date(1769900400000+0100)/",
            "einddatum": "/Date(1869900400000+0100)/",
            "functieBuitenRM": "Rechter-plaatsvervanger",
            "instantieBuitenRM": "Rechtbank Amsterdam",
        }
        response = {
            "completeDateTime": "/Date(1777637082369+0200)/",
            "errorMessage": None,
            "model": {
                "achternaam": "Test",
                "beroepsgegevensBuitenRM": [pd],
                "toonNaam": "mw. mr. drs. A.B. Test",
            },
            "status": 1,
            "validationMessages": None,
        }
        requests_mock.get(person_details_url(person.rechtspraak_id), json=response, status_code=200)

        assert person.professional_detail == []
        assert len(ProfessionalDetail.query.all()) == 0

        with RechtspraakScrapeSession() as session:
            enrich_person(session, person)

        assert len(person.professional_detail) == 1
        assert len(ProfessionalDetail.query.all()) == 1

        assert person.professional_detail[0].function == pd.get("functieBuitenRM")
        assert person.professional_detail[0].start_date == datetime(2026, 2, 1, 0, 0)
        assert person.professional_detail[0].end_date == datetime(2029, 4, 3, 10, 46, 40)
        assert person.professional_detail[0].remarks == pd.get("opmerkingen")
        assert person.professional_detail[0].organisation == pd.get("instantieBuitenRM")
        assert person.professional_detail[0].outside_of_judiciary is True


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
