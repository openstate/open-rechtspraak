from flask import url_for


def test_sitemap(client):
    r = client.get(url_for("flask_sitemap.sitemap"))
    assert r.status_code == 200


def test_unprotected_person_in_sitemap(client, person):
    r = client.get("/sitemap.xml")
    assert str(person.id) in r.get_data(as_text=True)


def test_protected_person_not_in_sitemap(client, protected_person):
    r = client.get("/sitemap.xml")
    assert str(protected_person.id) not in r.get_data(as_text=True)
