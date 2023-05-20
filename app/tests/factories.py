import factory

from app.database import db
from app.models import Person, Verdict


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        abstract = True


class PersonFactory(BaseFactory):
    class Meta:
        model = Person
        sqlalchemy_session = db.session

    initials = "A.B.C."
    titles = "prof. dr. mr."
    last_name = factory.Faker("last_name")
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

    ecli = "ECLI:NL:TEST:2020:1"
    title = factory.LazyAttribute(lambda a: "{}".format(a.ecli))
    raw_xml = "<?xml><rdf:description></rdf:rdf></open-rechtspraak>"
