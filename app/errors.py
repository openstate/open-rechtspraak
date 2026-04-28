from flask import render_template


def unauthorized_error(e: Exception) -> tuple[str, int]:
    return render_template("pages/error.html"), 401


def page_not_found(e: Exception) -> tuple[str, int]:
    return render_template("pages/error.html"), 404


def internal_server_error(e: Exception) -> tuple[str, int]:
    return render_template("pages/error.html"), 500


class EnrichError(Exception):
    pass
