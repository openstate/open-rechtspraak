import pytest
from pytest_factoryboy import register

import app.tests.factories as f
from app.app import create_app
from app.database import db as db_


def init_db():
    db_.drop_all()
    db_.create_all()


@pytest.fixture
def client(app):
    context = app.test_request_context()
    context.push()
    return app.test_client()


@pytest.fixture(scope="session")
def db(app):
    """Get a database instance"""
    return db_


@pytest.fixture(scope="session")
def app():
    app_ = create_app("test")
    with app_.app_context():
        init_db()
        yield app_


@pytest.fixture(scope="function", autouse=True)
def session(db, request):
    db.session.begin_nested()

    def teardown():
        db.session.rollback()
        db.session.close()

    request.addfinalizer(teardown)
    return db.session


register(f.PersonFactory)
