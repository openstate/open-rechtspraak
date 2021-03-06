from flask import Blueprint, jsonify, request

from app.models import Person

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route("/person/search")
def person_search():
    q = request.args.get("q", None)
    limit = request.args.get("limit", default=20, type=int)

    if limit > 100:
        limit = 20

    offset = request.args.get("offset", type=int)
    query = Person.query.filter(Person.protected.isnot(True))

    if q:
        query = query.filter(Person.toon_naam.ilike(f"%{q}%"))

    return jsonify(
        data=[
            person.serialize
            for person in query.order_by(Person.last_name.asc())
            .offset(offset)
            .limit(limit)
            .all()
        ],
        count=query.count(),
    )
