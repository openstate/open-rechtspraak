from tests.factories import VerdictFactory


def test_verdict_detail(client):
    verdict = VerdictFactory().save()
    r = client.get(f"/verdict/{verdict.id}")
    assert r.status_code == 200


def test_verdict_detail_by_ecli(client):
    verdict = VerdictFactory().save()
    r = client.get(f"/verdict/ecli/{verdict.ecli}")
    assert r.status_code == 200
