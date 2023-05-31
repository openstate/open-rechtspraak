from flask import url_for

from app.tests.factories import PersonFactory


class TestGeneral:
    def test_search(self, client):
        r = client.get(url_for("api.person"))
        assert r.status_code == 200

    def test_search_contains_person(self, client, person):
        r = client.get(url_for("api.person"))
        response_data = r.get_json().get("data")
        assert len(response_data) == 1
        assert response_data[0].get("id") == str(person.id)
        assert response_data[0].get("last_name") == person.last_name


class TestSearchParameter:
    def test_search_query(self, client, person):
        not_found_person = PersonFactory()
        params = {"q": person.last_name}
        r = client.get(url_for("api.person"), query_string=params)
        response_data = r.get_json().get("data")
        assert len(response_data) == 1
        assert response_data[0].get("last_name") == person.last_name
        assert response_data[0].get("last_name") != not_found_person.last_name


class TestOffsetLimit:
    def test_limit(self, client):
        PersonFactory.create_batch(5)

        params = {"limit": 1}
        r = client.get(url_for("api.person"), query_string=params)

        response_json = r.get_json()
        response_data = response_json.get("data")

        assert len(response_data) == 1

    def test_offset_limit(self, client):
        PersonFactory.create_batch(2)

        params = {"limit": 1, "offset": 0}
        r = client.get(url_for("api.person"), query_string=params)
        person_id = r.get_json().get("data")[0].get("id")

        params = {"limit": 1, "offset": 1}
        r = client.get(url_for("api.person"), query_string=params)
        second_person_id = r.get_json().get("data")[0].get("id")
        assert person_id != second_person_id


class TestProtectedPerson:
    def test_protected_person_is_hidden(self, client, protected_person):
        r = client.get(url_for("api.person"))
        response_data = r.get_json().get("data")

        for p in response_data:
            assert p.get("last_name") != protected_person.last_name


class TestCount:
    def test_count_without_search_parameter(self, client):
        count = 5
        PersonFactory.create_batch(count)
        r = client.get(url_for("api.person"))

        assert r.get_json().get("count") == count

    def test_count_with_search_parameter(self, client):
        people = PersonFactory.create_batch(5)

        params = {"q": people[0].toon_naam}
        r = client.get(url_for("api.person"), query_string=params)

        assert r.get_json().get("count") == 1


class TestFormerJudgeQueryParameter:
    def test_search_by_default_removed_at_are_not_included(
        self, client, removed_person
    ):
        r = client.get(url_for("api.person"))
        response_data = r.get_json().get("data")

        for p in response_data:
            assert p.get("last_name") != removed_person.last_name

    def test_search_former_judges_may_be_included_with_query_param(
        self, client, removed_person
    ):
        params = {"former_judges": "true"}
        r = client.get(url_for("api.person"), query_string=params)
        response_data = r.get_json().get("data")

        for p in response_data:
            assert p.get("last_name") == removed_person.last_name

    def test_search_former_judges_excluded_when_false(self, client, removed_person):
        params = {"former_judges": "false"}
        r = client.get(url_for("api.person"), query_string=params)
        response_data = r.get_json().get("data")

        for p in response_data:
            assert p.get("last_name") != removed_person.last_name
