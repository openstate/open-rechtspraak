import pytest
from pytest_factoryboy import register

import tests.factories as f
from app.app import create_app
from app.database import db as db_


def init_db():
    db_.drop_all()
    db_.create_all()


@pytest.fixture
def client(app):
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
