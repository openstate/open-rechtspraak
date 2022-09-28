from flask import Blueprint, jsonify, request

from app.api.filters import PersonFilterService
from app.api.serializers import person_list_serializer

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route("/person")
def person():
    service = PersonFilterService(request.args)
    service.apply_filters()
    count = service.query.count()
    service.apply_pagination()

    return jsonify(
        data=[person_list_serializer(item) for item in service.query.all()],
        count=count,
    )
