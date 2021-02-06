from flask import Blueprint, jsonify, render_template, request

from app.models import People

base_bp = Blueprint("base", __name__)


@base_bp.route("/")
def index():
    return render_template("pages/index.html")


@base_bp.route("/about")
def about():
    return render_template("pages/about.html")


api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route("/search")
def search():
    q = request.args.get("q", None)
    query = People.query

    if q:
        query = query.filter(People.toon_naam.ilike(f"%{q}%"))

    return jsonify(
        data=[person.serialize for person in query.limit(100).all()],
        count=query.count(),
    )
