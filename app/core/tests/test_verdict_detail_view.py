from flask import url_for
from requests.status_codes import codes


def test_verdict_detail(client, verdict):
    r = client.get(url_for("base.verdict_detail", id=verdict.id))
    assert r.status_code == codes.OK


def test_verdict_detail_by_ecli(client, verdict):
    r = client.get(url_for("base.verdict_by_ecli", ecli=verdict.ecli))
    assert r.status_code == codes.OK
