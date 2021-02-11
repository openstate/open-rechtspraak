from flask import Blueprint, jsonify, request

from app.models import People

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route("/search")
def search():
    q = request.args.get("q", None)
    limit = request.args.get("limit", default=20, type=int)

    if limit > 100:
        limit = 20

    offset = request.args.get("offset", type=int)
    query = People.query.filter(People.protected.isnot(True))

    if q:
        query = query.filter(People.toon_naam.ilike(f"%{q}%"))

    return jsonify(
        data=[
            person.serialize
            for person in query.order_by(People.last_name.asc())
            .offset(offset)
            .limit(limit)
            .all()
        ],
        count=query.count(),
    )
