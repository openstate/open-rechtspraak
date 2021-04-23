from flask import url_for

from tests.factories import PersonFactory


def test_search(client):
    r = client.get(url_for("api.person_search"))
    assert r.status_code == 200


def test_search_contains_person(client):
    person = PersonFactory()
    r = client.get(url_for("api.person_search"))
    response_data = r.get_json().get("data")
    assert len(response_data) == 1
    assert response_data[0].get("id") == str(person.id)
    assert response_data[0].get("last_name") == person.last_name


def test_search_query(client):
    found_person = PersonFactory().save()
    not_found_person = PersonFactory().save()
    params = {"q": found_person.last_name}
    r = client.get(url_for("api.person_search"), query_string=params)
    response_data = r.get_json().get("data")
    assert len(response_data) == 1
    assert response_data[0].get("last_name") == found_person.last_name
    assert response_data[0].get("last_name") != not_found_person.last_name


def test_search_limit(client):
    params = {"limit": 1}
    r = client.get(url_for("api.person_search"), query_string=params)
    response_data = r.get_json().get("data")
    assert len(response_data) == 1


def test_offset_limit(client):
    params = {"limit": 1, "offset": 0}
    r = client.get(url_for("api.person_search"), query_string=params)
    person_id = r.get_json().get("data")[0].get("id")

    params = {"limit": 1, "offset": 1}
    r = client.get(url_for("api.person_search"), query_string=params)
    second_person_id = r.get_json().get("data")[0].get("id")
    assert person_id != second_person_id


def test_search_protected_person_is_hidden(client):
    PersonFactory().save()
    hidden_person = PersonFactory(protected=True).save()
    r = client.get(url_for("api.person_search"))
    response_data = r.get_json().get("data")

    for p in response_data:
        assert p.get("last_name") != hidden_person.last_name
