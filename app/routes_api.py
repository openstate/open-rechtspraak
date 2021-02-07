from flask import Blueprint, jsonify, request

from app.models import People

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route("/search")
def search():
    q = request.args.get("q", None)
    query = People.query.filter(People.protected.isnot(True))

    if q:
        query = query.filter(People.toon_naam.ilike(f"%{q}%"))

    return jsonify(
        data=[person.serialize for person in query.limit(100).all()],
        count=query.count(),
    )
