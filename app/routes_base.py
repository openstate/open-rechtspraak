from flask import Blueprint, abort, render_template

from app.models import People, ProfessionalDetails, SideJobs

base_bp = Blueprint("base", __name__)


@base_bp.route("/")
def index():
    return render_template("pages/index.html")


@base_bp.route("/about")
def about():
    return render_template("pages/about.html")


@base_bp.route("/person/<id>")
def person_detail(id):
    person = People.query.filter(People.id == id).first()

    if person.protected:
        abort(404)

    professional_details = (
        ProfessionalDetails.query.filter(ProfessionalDetails.person_id == person.id)
        .filter(ProfessionalDetails.end_date.is_(None))
        .all()
    )
    historical_professional_details = (
        ProfessionalDetails.query.filter(ProfessionalDetails.person_id == person.id)
        .filter(ProfessionalDetails.end_date.isnot(None))
        .all()
    )
    side_jobs = (
        SideJobs.query.filter(SideJobs.person_id == person.id)
        .filter(SideJobs.end_date.is_(None))
        .all()
    )
    historical_side_jobs = (
        SideJobs.query.filter(SideJobs.person_id == person.id)
        .filter(SideJobs.end_date.isnot(None))
        .all()
    )
    return render_template(
        "person/detail.html",
        person=person,
        professional_details=professional_details,
        historical_professional_details=historical_professional_details,
        side_jobs=side_jobs,
        historical_side_jobs=historical_side_jobs,
    )
