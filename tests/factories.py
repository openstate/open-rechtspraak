import factory

from app.database import db
from app.models import Person


class PersonFactory(factory.alchemy.SQLAlchemyModelFactory):
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
