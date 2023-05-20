import random

import click
import factory
from flask.cli import with_appcontext

from app.models import Person, PersonVerdict, Verdict
from app.tests import factories


def seed_people(n: int = 10):
    people = [
        factory.build(dict, FACTORY_CLASS=factories.PersonFactory) for i in range(n)
    ]
    return [Person.update_or_create(person) for person in people]


def seed_verdicts(n: int = 30):
    verdicts = [
        factory.build(dict, FACTORY_CLASS=factories.VerdictFactory) for i in range(n)
    ]
    return [Verdict.update_or_create(verdict) for verdict in verdicts]


@click.command("seed")
@with_appcontext
def seed():
    people = seed_people()

    verdicts = seed_verdicts()
    for verdict in verdicts:
        # select 1, 3 or 5 judges that will be related to the verdict
        related_judges = random.choices(people, k=random.choice([1, 3, 5]))
        for person in related_judges:
            PersonVerdict.create(
                role="rechter", verdict_id=verdict.id, person_id=person.id
            )
