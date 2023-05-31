from app.models import Institution
from app.scraper.other.config import INSTITUTIONS_URL
from app.scraper.other.institutions import import_institutions_handler
from app.scraper.other.tests.fixtures import (
    FIVE_INSTITUTIONS_XML,
    NO_INSTITUTIONS_XML,
    ONE_INSTITUTION_XML,
)


def test_request_creates_institution(requests_mock):
    requests_mock.get(INSTITUTIONS_URL, status_code=200, text=ONE_INSTITUTION_XML)

    assert Institution.query.count() == 0
    import_institutions_handler()
    assert Institution.query.count() == 1


def test_institution_attributes_are_mapped_correctly(requests_mock):
    requests_mock.get(INSTITUTIONS_URL, status_code=200, text=ONE_INSTITUTION_XML)

    import_institutions_handler()
    institution = Institution.query.first()

    assert institution.name == "Ambtenarengerecht Amsterdam"
    assert institution.abbrevation == "AGAMS"
    assert institution.lido_id == "http://psi.rechtspraak.nl/agam"


def test_request_creates_multiple_institutions(requests_mock):
    requests_mock.get(INSTITUTIONS_URL, status_code=200, text=FIVE_INSTITUTIONS_XML)

    assert Institution.query.count() == 0
    import_institutions_handler()
    assert Institution.query.count() == 5


def test_only_one_institution_is_created_on_subsequent_scrapes(requests_mock):
    requests_mock.get(INSTITUTIONS_URL, status_code=200, text=ONE_INSTITUTION_XML)

    assert Institution.query.count() == 0
    import_institutions_handler()
    assert Institution.query.count() == 1
    import_institutions_handler()
    assert Institution.query.count() == 1


def test_no_institution_is_created(requests_mock):
    requests_mock.get(INSTITUTIONS_URL, status_code=200, text=NO_INSTITUTIONS_XML)

    assert Institution.query.count() == 0
    import_institutions_handler()
    assert Institution.query.count() == 0
