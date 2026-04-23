from flask import url_for
from requests.status_codes import codes


def test_index(client):
    r = client.get(url_for("base.index"))
    assert r.status_code == codes.OK


def test_about(client):
    r = client.get(url_for("base.about"))
    assert r.status_code == codes.OK


def test_apidocs(client):
    r = client.get(url_for("base.api_docs"))
    assert r.status_code == codes.OK
