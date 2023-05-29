from datetime import datetime, timedelta

from app.models import Verdict
from app.scraper.verdicts.config import SEARCH_ENDPOINT
from app.scraper.verdicts.import_verdicts import import_verdicts_handler
from app.scraper.verdicts.tests.fixtures import (
    FIVE_VERDICTS_ATOM,
    NO_VERDICTS_ATOM,
    ONE_VERDICT_ATOM,
)

START_DATETIME = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S")
END_DATETIME = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def test_import_creates_one_verdict(requests_mock):
    requests_mock.get(SEARCH_ENDPOINT, status_code=200, text=ONE_VERDICT_ATOM)

    import_verdicts_handler(START_DATETIME, END_DATETIME)
    assert Verdict.query.count() == 1


def test_attributes_are_mapped_correctly(requests_mock):
    requests_mock.get(SEARCH_ENDPOINT, status_code=200, text=ONE_VERDICT_ATOM)

    import_verdicts_handler(START_DATETIME, END_DATETIME)
    verdict = Verdict.query.first()

    assert verdict.ecli == "ECLI:NL:RVS:2000:AA5654"
    assert (
        verdict.title
        == "ECLI:NL:RVS:2000:AA5654, Raad van State, 20-04-2000, 19990054111"
    )
    assert verdict.summary == "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    assert (
        verdict.uri
        == "https://uitspraken.rechtspraak.nl/InzienDocument?id=ECLI:NL:RVS:2000:AA5654"
    )


def test_import_creates_multiple_verdicts(requests_mock):
    requests_mock.get(SEARCH_ENDPOINT, status_code=200, text=FIVE_VERDICTS_ATOM)

    import_verdicts_handler(START_DATETIME, END_DATETIME)
    assert Verdict.query.count() == 5


def test_import_creates_no_verdicts(requests_mock):
    requests_mock.get(SEARCH_ENDPOINT, status_code=200, text=NO_VERDICTS_ATOM)

    import_verdicts_handler(START_DATETIME, END_DATETIME)
    assert Verdict.query.count() == 0


def test_import_error_creates_no_verdicts(requests_mock):
    requests_mock.get(SEARCH_ENDPOINT, status_code=500, text=ONE_VERDICT_ATOM)

    import_verdicts_handler(START_DATETIME, END_DATETIME)
    assert Verdict.query.count() == 0


def test_only_one_verdict_is_created_on_subsequent_scrapes(requests_mock):
    requests_mock.get(SEARCH_ENDPOINT, status_code=200, text=ONE_VERDICT_ATOM)

    assert Verdict.query.count() == 0
    import_verdicts_handler(START_DATETIME, END_DATETIME)
    assert Verdict.query.count() == 1
    import_verdicts_handler(START_DATETIME, END_DATETIME)
    assert Verdict.query.count() == 1
