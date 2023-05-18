import random
import string
from datetime import datetime, timedelta

import click
from faker import Faker
from flask.cli import with_appcontext

from app.database import db
from app.models import Person
from app.scraper.other.institutions import import_institutions_handler
from app.scraper.other.legal_areas import import_legal_areas_handler
from app.scraper.other.procedure_types import import_procedure_types_handler
from app.scraper.people.extract import enrich_people_handler, import_people_handler
from app.scraper.verdicts.extract import (
    enrich_verdicts_handler,
    import_verdicts_handler,
)


@click.command("placeholder")
@with_appcontext
def placeholder():
    print("Still here!")


@click.command("import_people")
@with_appcontext
def import_people():
    import_people_handler()


@click.command("enrich_people")
@with_appcontext
def enrich_people():
    enrich_people_handler()


@click.command("import_verdicts")
@click.option("--start_date", default=None)
@click.option("--end_date", default=None)
@with_appcontext
def import_verdicts(start_date, end_date):
    if not start_date:
        start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    import_verdicts_handler(start_date, end_date)


@click.command("enrich_verdicts")
@with_appcontext
def enrich_verdicts():
    enrich_verdicts_handler()


def person_generator():
    fake = Faker()
    initials = fake.first_name()[0]
    titles = fake.prefix()
    last_name = fake.last_name()
    return {
        "titles": titles,
        "last_name": last_name,
        "gender": random.choice(["male", "female"]),
        "toon_naam": titles + " " + initials + " " + last_name,
        "toon_naam_kort": initials + " " + last_name,
        "rechtspraak_id": "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        ),
    }


@click.command("seed")
@with_appcontext
def seed():
    people = [person_generator() for i in range(0, 10)]
    for person in people:
        Person.update_or_create(person)


@click.command("db_truncate")
@with_appcontext
def db_truncate():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print("Clear table %s" % table)
        db.session.execute(table.delete())
    db.session.commit()


@click.command("import_institutions")
@with_appcontext
def import_institutions():
    import_institutions_handler()


@click.command("import_procedure_types")
@with_appcontext
def import_procedure_types():
    import_procedure_types_handler()


@click.command("import_legal_areas")
@with_appcontext
def import_legal_areas():
    import_legal_areas_handler()
