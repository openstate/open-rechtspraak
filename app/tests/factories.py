import random

import factory
from factory import fuzzy

from app.database import db
from app.models import Person, Verdict


def generate_ecli():
    year = random.randrange(2000, 2030)
    case_number = random.randrange(0, 10000)
    return f"ECLI:NL:TEST:{year}:{case_number}"


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        abstract = True


class PersonFactory(BaseFactory):
    class Meta:
        model = Person
        sqlalchemy_session = db.session

    first_name = factory.Faker("first_name")
    initials = factory.LazyAttribute(lambda a: "{}.".format(a.first_name[0]))
    titles = factory.Faker("prefix")
    last_name = factory.Faker("last_name")
    gender = fuzzy.FuzzyChoice(["male", "female"])
    rechtspraak_id = factory.Faker("md5")
    toon_naam = factory.LazyAttribute(
        lambda a: "{} {} {}".format(a.titles, a.initials, a.last_name)
    )
    toon_naam_kort = factory.LazyAttribute(
        lambda a: "{} {}".format(a.initials, a.last_name)
    )
    protected = False
    removed_from_rechtspraak_at = None


class VerdictFactory(BaseFactory):
    class Meta:
        model = Verdict

    ecli = factory.LazyAttribute(lambda x: generate_ecli())
    title = factory.LazyAttribute(lambda a: "{}".format(a.ecli))
    issued = factory.Faker("date")
    raw_xml = "<?xml><rdf:description></rdf:rdf></open-rechtspraak>"
