from flask import Blueprint, abort, jsonify, redirect, request, url_for

from app.api.serializers import person_list_serializer, verdict_serializer
from app.api.services import PersonService, PersonVerdictsService
from app.models import Person
from app.util import is_valid_uuid

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route("/")
def redirect_api_docs():
    return redirect(url_for("base.api_docs"))


@api_bp.route("/person")
def person():
    service = PersonService(request.args)
    service.apply_filtering()

    count = service.queryset.count()

    service.apply_ordering()
    service.apply_pagination()
    people = service.queryset.all()

    return jsonify(
        data=[person_list_serializer(item) for item in people],
        count=count,
    )


@api_bp.route("/person/<id>/verdicts")
def person_verdicts(id):
    if not is_valid_uuid(id):
        abort(404)

    person = Person.query.filter(Person.id == id).first()

    if not person or person.protected:
        abort(404)

    service = PersonVerdictsService(person, request.args)
    count = service.queryset.count()

    service.apply_ordering()
    service.apply_pagination()
    verdicts = service.queryset.all()

    return jsonify(
        data=[verdict_serializer(item) for item in verdicts],
        count=count,
    )
