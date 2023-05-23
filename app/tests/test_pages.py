from flask import url_for


def test_index(client):
    r = client.get(url_for("base.index"))
    assert r.status_code == 200


def test_about(client):
    r = client.get(url_for("base.about"))
    assert r.status_code == 200


def test_apidocs(client):
    r = client.get(url_for("base.api_docs"))
    assert r.status_code == 200
