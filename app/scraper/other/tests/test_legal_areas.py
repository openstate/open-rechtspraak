from app.models import LegalArea
from app.scraper.other.config import LEGAL_AREAS_URL
from app.scraper.other.legal_areas import import_legal_areas_handler
from app.scraper.other.tests.fixtures import (
    NO_LEGAL_AREAS_XML,
    ONE_MAIN_AND_ONE_SUB_LEGAL_AREA_XML,
    TWO_MAIN_AND_TWO_SUB_LEGAL_AREAS_XML,
)


def test_request_creates_legal_area(requests_mock):
    requests_mock.get(
        LEGAL_AREAS_URL, status_code=200, text=ONE_MAIN_AND_ONE_SUB_LEGAL_AREA_XML
    )

    assert LegalArea.query.count() == 0
    import_legal_areas_handler()
    assert LegalArea.query.count() == 2


def test_legal_area_attributes_are_mapped_correctly(requests_mock):
    requests_mock.get(
        LEGAL_AREAS_URL, status_code=200, text=ONE_MAIN_AND_ONE_SUB_LEGAL_AREA_XML
    )

    import_legal_areas_handler()
    legal_area = LegalArea.query.first()

    assert legal_area.legal_area_name == "Bestuursrecht"
    assert (
        legal_area.legal_area_lido_id
        == "http://psi.rechtspraak.nl/rechtsgebied#bestuursrecht"
    )


def test_request_creates_multiple_legal_areas(requests_mock):
    requests_mock.get(
        LEGAL_AREAS_URL, status_code=200, text=TWO_MAIN_AND_TWO_SUB_LEGAL_AREAS_XML
    )

    assert LegalArea.query.count() == 0
    import_legal_areas_handler()
    assert LegalArea.query.count() == 6


def test_only_one_legal_area_is_created_on_subsequent_scrapes(requests_mock):
    requests_mock.get(
        LEGAL_AREAS_URL, status_code=200, text=ONE_MAIN_AND_ONE_SUB_LEGAL_AREA_XML
    )

    assert LegalArea.query.count() == 0
    import_legal_areas_handler()
    assert LegalArea.query.count() == 2
    import_legal_areas_handler()
    assert LegalArea.query.count() == 2


def test_no_legal_area_is_created(requests_mock):
    requests_mock.get(LEGAL_AREAS_URL, status_code=200, text=NO_LEGAL_AREAS_XML)

    assert LegalArea.query.count() == 0
    import_legal_areas_handler()
    assert LegalArea.query.count() == 0
