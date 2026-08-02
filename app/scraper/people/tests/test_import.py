from app.models import Person
from app.scraper.people.import_people import update_or_create_person
from app.tests.factories import PersonFactory


def test_person_gets_created_by_persoon_id(requests_mock, person):
    """This test ensures that a scraped person is created if their toonnaam does not exist yet."""
    scraped_person = {
        "id": "61010c72ca77-68e6-4388-8f8d-f55e6f6f",
        "samengesteldeNaam": "mr. dr. van der Achternaam",
    }
    assert scraped_person.get("samengesteldeNaam") != person.toon_naam
    assert Person.query.count() == 1

    created_person = update_or_create_person(scraped_person)

    assert Person.query.count() == 2
    assert created_person.toon_naam == scraped_person.get("samengesteldeNaam")


def test_person_gets_updated_if_persoon_id_is_identical(requests_mock):
    """This test ensures that attributes (i.e. last name) of a person are updated if they are rescraped, assuming
    their id is identical.
    """
    rechtspraak_id = "61010c72ca77-68e6-4388-8f8d-f55e6f6f"
    person = PersonFactory(rechtspraak_id=rechtspraak_id)

    new_name = "mr. dr. L.J.S. van der Achternaam"
    new_initials = "L.J.S."
    new_last_name = "van der Achternaam"

    scraped_person = {
        "id": rechtspraak_id,
        "samengesteldeNaam": new_name,
    }

    assert person.last_name != new_last_name
    assert person.toon_naam != new_name
    assert person.initials != new_initials
    assert rechtspraak_id == person.rechtspraak_id

    assert Person.query.count() == 1
    update_or_create_person(scraped_person)

    queried_person = Person.query.first()
    assert queried_person.last_name == new_last_name
    assert queried_person.toon_naam == new_name
    assert queried_person.initials == new_initials
    assert Person.query.count() == 1
