from tests.factories import PersonFactory


def test_list_search(client):
    r = client.get("/api/v1/search")
    assert r.status_code == 200


def test_list_search_contains_person(client):
    person = PersonFactory()
    r = client.get("/api/v1/search")
    response_data = r.get_json().get("data")
    assert len(response_data) == 1
    assert response_data[0].get("id") == str(person.id)
    assert response_data[0].get("last_name") == person.last_name


def test_list_search_query(client):
    found_person = PersonFactory().save()
    not_found_person = PersonFactory().save()
    params = {"q": found_person.last_name}
    r = client.get("/api/v1/search", query_string=params)
    response_data = r.get_json().get("data")
    assert len(response_data) == 1
    assert response_data[0].get("last_name") == found_person.last_name
    assert response_data[0].get("last_name") != not_found_person.last_name


def test_list_protected_person_is_hidden(client):
    PersonFactory().save()
    hidden_person = PersonFactory(protected=True).save()
    r = client.get("/api/v1/search")
    response_data = r.get_json().get("data")

    for p in response_data:
        assert p.get("last_name") != hidden_person.last_name
