from flask import Blueprint, jsonify, redirect, render_template, request

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


redirect_bp = Blueprint("redirect", __name__, url_prefix="/redirect")


@redirect_bp.route("/rechtspraak/open-data")
def rechtspraak_open_data():
    return redirect("https://www.rechtspraak.nl/Uitspraken/paginas/open-data.aspx")


@redirect_bp.route("/rechtspraak/search")
def rechtspraak_search():
    return redirect("https://namenlijst.rechtspraak.nl/")


@redirect_bp.route("/rechtspraak/persoon/<id>")
def rechtspraak_persoon(id):
    return redirect(f"https://namenlijst.rechtspraak.nl/#!/details/{id}")
