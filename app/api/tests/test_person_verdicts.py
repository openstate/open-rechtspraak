from flask import url_for


def test_endpoint(client, person_with_verdict):
    r = client.get(url_for("api.person_verdicts", id=person_with_verdict.id))
    assert r.status_code == 200


def test_contains_one_verdict(client, person_with_verdict):
    r = client.get(url_for("api.person_verdicts", id=person_with_verdict.id))
    response_json = r.get_json()
    response_data = response_json.get("data")

    verdict = person_with_verdict.verdicts[0].verdict

    assert response_json.get("count") == 1
    assert len(response_data) == 1
    assert response_data[0].get("id") == str(verdict.id)
    assert response_data[0].get("ecli") == verdict.ecli


def test_contains_verdicts(client, person_with_verdicts):
    r = client.get(url_for("api.person_verdicts", id=person_with_verdicts.id))
    response_json = r.get_json()
    response_data = response_json.get("data")

    verdicts = person_with_verdicts.verdicts

    assert response_json.get("count") == len(verdicts)
    assert len(response_data) == len(verdicts)

    for pv in verdicts:
        verdict = pv.verdict
        assert str(verdict.id) in [i.get("id") for i in response_data]
        assert verdict.ecli in [i.get("ecli") for i in response_data]


def test_limit(client, person_with_verdicts):
    params = {"limit": 1}
    r = client.get(
        url_for("api.person_verdicts", id=person_with_verdicts.id), query_string=params
    )

    response_json = r.get_json()
    response_data = response_json.get("data")

    verdicts = person_with_verdicts.verdicts

    assert response_json.get("count") == len(verdicts)
    assert len(response_data) != len(verdicts)


def test_offset_limit(client, person_with_verdicts):
    params = {"limit": 1, "offset": 0}
    r = client.get(
        url_for("api.person_verdicts", id=person_with_verdicts.id), query_string=params
    )
    verdict_id = r.get_json().get("data")[0].get("id")

    params = {"limit": 1, "offset": 1}
    r = client.get(
        url_for("api.person_verdicts", id=person_with_verdicts.id), query_string=params
    )
    second_verdict_id = r.get_json().get("data")[0].get("id")
    assert verdict_id != second_verdict_id


def test_protected_person_is_hidden(client, protected_person):
    r = client.get(url_for("api.person_verdicts", id=protected_person.id))
    assert r.status_code == 404


def test_illegal_id(client, person):
    illegal_id = "abc"
    r = client.get(url_for("api.person_verdicts", id=illegal_id))
    assert r.status_code == 404
