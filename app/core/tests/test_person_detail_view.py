from flask import url_for


def test_person_detail(client, person):
    r = client.get(url_for("base.person_detail", id=person.id))
    assert r.status_code == 200


def test_person_detail_not_allowed_for_protected(client, protected_person):
    r = client.get(url_for("base.person_detail", id=protected_person.id))
    assert r.status_code == 404
