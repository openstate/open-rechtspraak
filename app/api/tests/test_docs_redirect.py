from flask import url_for


def test_api_base_redirects_to_docs(client):
    r = client.get(url_for("api.redirect_api_docs"))
    assert r.status_code == 302

    r = client.get(url_for("api.redirect_api_docs"), follow_redirects=True)
    assert r.request.path == url_for("base.api_docs")
