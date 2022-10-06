from flask import url_for

from app.tests.factories import VerdictFactory


def test_verdict_detail(client):
    verdict = VerdictFactory().save()
    r = client.get(url_for("base.verdict_detail", id=verdict.id))
    assert r.status_code == 200


def test_verdict_detail_by_ecli(client):
    verdict = VerdictFactory().save()
    r = client.get(url_for("base.verdict_by_ecli", ecli=verdict.ecli))
    assert r.status_code == 200
