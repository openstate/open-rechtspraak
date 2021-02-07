from tests.factories import PersonFactory


def test_detail(client):
    person = PersonFactory().save()
    r = client.get(f"/person/{person.id}")
    assert r.status_code == 200


def test_detail_not_allowed_for_protected(client):
    person = PersonFactory(protected=True).save()
    r = client.get(f"/person/{person.id}")
    assert r.status_code == 404
