import pytest
from pytest_factoryboy import register

import app.tests.factories as f
from app.app import create_app
from app.database import db as db_


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


@pytest.fixture(autouse=True)
def db_session(app):
    db_.app = app
    with app.app_context():
        db_.create_all()

    yield db_

    db_.session.close()
    db_.drop_all()


register(f.PersonFactory)
