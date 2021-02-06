from flask import render_template


def unauthorized_error(e):
    return render_template("pages/error.html"), 401


def page_not_found(e):
    return render_template("pages/error.html"), 404


def internal_server_error(e):
    return render_template("pages/error.html"), 500
