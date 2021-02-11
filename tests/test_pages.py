def test_index(client):
    r = client.get("/")
    assert r.status_code == 200


def test_about(client):
    r = client.get("/about")
    assert r.status_code == 200
