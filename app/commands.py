import random
import string

import click
from faker import Faker
from flask.cli import with_appcontext

from app.models import People
from app.scraper.extract import collect_and_save_people


@click.command("placeholder")
@with_appcontext
def placeholder():
    print("Still here!")


@click.command("import_people")
@with_appcontext
def import_people():
    collect_and_save_people()


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
        People.update_or_create(person)
