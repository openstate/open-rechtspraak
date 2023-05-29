from app.scraper.verdicts.utils import recognize_people


class TestRecognizePeople:
    def test_with_people_from_database(self, person, second_person):
        assert person.toon_naam != second_person.toon_naam

        text = f"Dit is een voorbeeldtekst met daarin de naam van {person.toon_naam}."
        found = recognize_people(text)

        assert len(found) == 1
        assert person in found
        assert second_person not in found

    def test_with_pre_given_list_of_people(self, person, second_person):
        assert person.toon_naam != second_person.toon_naam

        text = f"Dit is een voorbeeldtekst met daarin de naam van {person.toon_naam}."
        found = recognize_people(text, [person, second_person])

        assert len(found) == 1
        assert person in found
        assert second_person not in found

    def test_with_toon_naam_kort(self, person, second_person):
        assert person.toon_naam != second_person.toon_naam

        text = f"Dit is een voorbeeldtekst met daarin de korte naam van {person.toon_naam_kort}."
        found = recognize_people(text, [person, second_person])

        assert len(found) == 1
        assert person in found
        assert second_person not in found
