from app.models import Person
from app.scraper.people.import_people import update_or_create_person


def test_person_gets_created_by_persoon_id(requests_mock, person):
    """This test ensures that a scraped person is created if their toonnaam does not exist yet."""
    rechtspraak_internal_id = "7555d08769b89640"
    scraped_person = {
        "ACHTERNAAM": "Van der Achternaam",
        "SorteerAchternaam": "Achternaam",
        "functies": [],
        "persoonId": "L8ls0piIS4ywQ24-SE8BDnVV0IdpuJZA",
        "toonnaam": "Mr. Dr. van der Achternaam",
        "toonnaamkort": "A.B. van der Achternaam",
    }
    assert scraped_person.get("toonnaam") != person.toon_naam
    assert person.rechtspraak_internal_id != rechtspraak_internal_id
    assert Person.query.count() == 1

    created_person = update_or_create_person(scraped_person)

    assert Person.query.count() == 2
    assert created_person.toon_naam == scraped_person.get("toonnaam")
    assert created_person.rechtspraak_internal_id == rechtspraak_internal_id


def test_person_gets_updated_if_persoon_id_is_identical(requests_mock, person):
    """This test ensures that attributes (i.e. last name) of a person are updated if they are rescraped, assuming
    their 'rechtspraak_id' (persoonId) is identical.
    """
    new_last_name = "Van der Achternaam"
    new_toon_naam = "Van der Toonnaam"
    assert person.last_name != new_last_name
    assert person.toon_naam != new_toon_naam

    scraped_person = {
        "ACHTERNAAM": new_last_name,
        "SorteerAchternaam": person.last_name,
        "functies": [],
        "persoonId": person.rechtspraak_id,
        "toonnaam": new_toon_naam,
        "toonnaamkort": new_toon_naam,
    }

    assert Person.query.count() == 1
    update_or_create_person(scraped_person)

    queried_person = Person.query.first()
    assert queried_person.last_name == new_last_name
    assert queried_person.toon_naam == new_toon_naam
    assert queried_person.toon_naam_kort == new_toon_naam
    assert Person.query.count() == 1
