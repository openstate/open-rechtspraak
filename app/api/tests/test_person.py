from datetime import datetime

from flask import url_for

from app.tests.factories import PersonFactory


def test_search(client):
    r = client.get(url_for("api.person"))
    assert r.status_code == 200


def test_search_contains_person(client, person):
    r = client.get(url_for("api.person"))
    response_data = r.get_json().get("data")
    assert len(response_data) == 1
    assert response_data[0].get("id") == str(person.id)
    assert response_data[0].get("last_name") == person.last_name


def test_search_query(client, person):
    not_found_person = PersonFactory()
    params = {"q": person.last_name}
    r = client.get(url_for("api.person"), query_string=params)
    response_data = r.get_json().get("data")
    assert len(response_data) == 1
    assert response_data[0].get("last_name") == person.last_name
    assert response_data[0].get("last_name") != not_found_person.last_name


def test_search_limit(client):
    count = 5
    PersonFactory.create_batch(count)

    params = {"limit": 1}
    r = client.get(url_for("api.person"), query_string=params)

    response_json = r.get_json()
    response_data = response_json.get("data")

    assert response_json.get("count") == count
    assert len(response_data) == 1


def test_offset_limit(client):
    PersonFactory.create_batch(2)

    params = {"limit": 1, "offset": 0}
    r = client.get(url_for("api.person"), query_string=params)
    person_id = r.get_json().get("data")[0].get("id")

    params = {"limit": 1, "offset": 1}
    r = client.get(url_for("api.person"), query_string=params)
    second_person_id = r.get_json().get("data")[0].get("id")
    assert person_id != second_person_id


def test_search_protected_person_is_hidden(client, protected_person):
    r = client.get(url_for("api.person"))
    response_data = r.get_json().get("data")

    for p in response_data:
        assert p.get("last_name") != protected_person.last_name


def test_search_by_default_removed_at_are_not_included(client):
    removed_person = PersonFactory(removed_from_rechtspraak_at=datetime.now())
    r = client.get(url_for("api.person"))
    response_data = r.get_json().get("data")

    for p in response_data:
        assert p.get("last_name") != removed_person.last_name


def test_search_former_judges_may_be_included_with_query_param(client):
    removed_person = PersonFactory(removed_from_rechtspraak_at=datetime.now())

    params = {"former_judges": "true"}
    r = client.get(url_for("api.person"), query_string=params)
    response_data = r.get_json().get("data")

    for p in response_data:
        assert p.get("last_name") == removed_person.last_name
