from app.models import ProcedureType
from app.scraper.other.config import PROCEDURE_TYPES_URL
from app.scraper.other.procedure_types import import_procedure_types_handler
from app.scraper.other.tests.fixtures import (
    FIVE_PROCEDURE_TYPES_XML,
    NO_PROCEDURE_TYPES_XML,
    ONE_PROCEDURE_TYPE_XML,
)


def test_request_creates_procedure_type(requests_mock):
    requests_mock.get(PROCEDURE_TYPES_URL, status_code=200, text=ONE_PROCEDURE_TYPE_XML)

    assert ProcedureType.query.count() == 0
    import_procedure_types_handler()
    assert ProcedureType.query.count() == 1


def test_procedure_type_attributes_are_mapped_correctly(requests_mock):
    requests_mock.get(PROCEDURE_TYPES_URL, status_code=200, text=ONE_PROCEDURE_TYPE_XML)

    import_procedure_types_handler()
    procedure_type = ProcedureType.query.first()

    assert procedure_type.name == "Artikel 81 RO-zaken"
    assert (
        procedure_type.lido_id == "http://psi.rechtspraak.nl/procedure#artikel81ROzaken"
    )


def test_request_creates_multiple_procedure_types(requests_mock):
    requests_mock.get(
        PROCEDURE_TYPES_URL, status_code=200, text=FIVE_PROCEDURE_TYPES_XML
    )

    assert ProcedureType.query.count() == 0
    import_procedure_types_handler()
    assert ProcedureType.query.count() == 5


def test_only_one_procedure_type_is_created_on_subsequent_scrapes(requests_mock):
    requests_mock.get(PROCEDURE_TYPES_URL, status_code=200, text=ONE_PROCEDURE_TYPE_XML)

    assert ProcedureType.query.count() == 0
    import_procedure_types_handler()
    assert ProcedureType.query.count() == 1
    import_procedure_types_handler()
    assert ProcedureType.query.count() == 1


def test_no_procedure_type_is_created(requests_mock):
    requests_mock.get(PROCEDURE_TYPES_URL, status_code=200, text=NO_PROCEDURE_TYPES_XML)

    assert ProcedureType.query.count() == 0
    import_procedure_types_handler()
    assert ProcedureType.query.count() == 0
