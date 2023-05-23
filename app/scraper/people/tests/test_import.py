from app.models import Person
from app.scraper.people.import_people import update_or_create_person


def test_person_gets_created_if_no_toonaam_exists(requests_mock, person):
    """
    This test ensures that a scraped person is created if their toonnaam does not exist yet.
    """
    assert Person.query.count() == 1

    scraped_person = {
        "ACHTERNAAM": "Van der Achternaam",
        "SorteerAchternaam": "Achternaam",
        "functies": [],
        "persoonId": "abc-123",
        "toonnaam": "Mr. Dr. van der Achternaam",
        "toonnaamkort": "A.B. van der Achternaam",
    }
    assert scraped_person.get("toonnaam") != person.toon_naam

    created_person = update_or_create_person(scraped_person)

    assert Person.query.count() == 2
    assert created_person.toon_naam == scraped_person.get("toonnaam")


def test_person_gets_updated_if_toonnaam_is_identical(requests_mock, person):
    """
    This test ensures that attributes (i.e. last name) of a person are updated if they are rescraped, assuming
      their 'toonnaam' is identical.
    """
    new_last_name = "Van der Achternaam"
    assert person.last_name != new_last_name

    scraped_person = {
        "ACHTERNAAM": new_last_name,
        "SorteerAchternaam": person.last_name,
        "functies": [],
        "persoonId": person.rechtspraak_id,
        "toonnaam": person.toon_naam,
        "toonnaamkort": person.toon_naam_kort,
    }

    update_or_create_person(scraped_person)

    queried_person = Person.query.first()
    assert queried_person.last_name == new_last_name
    assert Person.query.count() == 1
