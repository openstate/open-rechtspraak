from tests.factories import PersonFactory


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200


def test_about(client):
    r = client.get("/about")
    assert r.status_code == 200


def test_sitemap(client):
    r = client.get("/sitemap.xml")
    assert r.status_code == 200


def test_unprotected_person_in_sitemap(client):
    person = PersonFactory().save()
    r = client.get("/sitemap.xml")
    assert str(person.id) in r.get_data(as_text=True)


def test_protected_person_not_in_sitemap(client):
    person = PersonFactory(protected=True).save()
    r = client.get("/sitemap.xml")
    assert str(person.id) not in r.get_data(as_text=True)
