from datetime import datetime

import pytest
from pytest_factoryboy import register

import app.tests.factories as f
from app.app import create_app
from app.database import db as db_
from app.models import Person, PersonVerdict, Verdict


@pytest.fixture
def client(app):
    context = app.test_request_context()
    context.push()
    return app.test_client()


@pytest.fixture(scope="session")
def app():
    app_ = create_app("test")
    with app_.app_context():
        yield app_


@pytest.fixture(scope="function", autouse=True)
def db(app):
    db_.app = app
    with app.app_context():
        db_.create_all()
        db_.session.commit()

    yield db_

    db_.session.close()
    db_.drop_all()


@pytest.fixture
def person() -> Person:
    return f.PersonFactory()


@pytest.fixture
def second_person() -> Person:
    return f.PersonFactory()


@pytest.fixture
def protected_person() -> Person:
    return f.PersonFactory(protected=True)


@pytest.fixture
def removed_person() -> Person:
    return f.PersonFactory(removed_from_rechtspraak_at=datetime.now())


@pytest.fixture
def verdict() -> Verdict:
    return f.Verdict()


@pytest.fixture
def person_with_verdict(person, verdict) -> Person:
    PersonVerdict.create(person_id=person.id, verdict_id=verdict.id, role="rechter")
    return person


@pytest.fixture
def person_with_verdicts(person) -> Person:
    verdicts = f.VerdictFactory.create_batch(5)
    for verdict in verdicts:
        PersonVerdict.create(person_id=person.id, verdict_id=verdict.id, role="rechter")
    return person


@pytest.fixture
def verdict_with_people() -> Verdict:
    verdict = f.VerdictFactory()
    people = f.PersonFactory.create_batch(3)
    for person in people:
        PersonVerdict.create(verdict_id=verdict.id, person_id=person.id, role="rechter")
    return verdict


register(f.PersonFactory)
register(f.VerdictFactory)
