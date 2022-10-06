from flask import url_for


def test_csp(client):
    r = client.get(url_for("base.index"))
    assert "Content-Security-Policy" in r.headers
    assert "unsafe" not in r.headers["Content-Security-Policy"]


def test_permissions_policy(client):
    r = client.get(url_for("base.index"))
    assert "Permissions-Policy" in r.headers


def test_feature_policy(client):
    r = client.get(url_for("base.index"))
    assert "Feature-Policy" in r.headers
