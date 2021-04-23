from flask import url_for

from tests.factories import PersonFactory


def test_person_detail(client):
    person = PersonFactory().save()
    r = client.get(url_for("base.person_detail", id=person.id))
    assert r.status_code == 200


def test_person_detail_not_allowed_for_protected(client):
    person = PersonFactory(protected=True).save()
    r = client.get(url_for("base.person_detail", id=person.id))
    assert r.status_code == 404
