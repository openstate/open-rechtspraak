from flask import Blueprint, abort, render_template

from app.models import Person, PersonVerdict, ProfessionalDetail, SideJob, Verdict
from app.verdict_scraper.soup_parsing import find_beslissing, to_soup

base_bp = Blueprint("base", __name__)


@base_bp.route("/")
def index():
    return render_template("pages/index.html")


@base_bp.route("/about")
def about():
    return render_template("pages/about.html")


@base_bp.route("/verdict/<id>")
def verdict_detail(id):
    verdict = Verdict.query.filter(Verdict.id == id).first()
    beslissing = find_beslissing(to_soup(verdict.raw_xml))
    related_people = (
        Person.query.join(Person.verdicts)
        .filter(PersonVerdict.verdict_id == verdict.id)
        .all()
    )
    return render_template(
        "verdicts/detail.html",
        verdict=verdict,
        beslissing=beslissing,
        related_people=related_people,
    )


@base_bp.route("/verdict/ecli/<ecli>")
def verdict_by_ecli(ecli):
    verdict = Verdict.query.filter(Verdict.ecli == ecli).first()
    return verdict_detail(verdict.id)


@base_bp.route("/person/<id>")
def person_detail(id):
    person = Person.query.filter(Person.id == id).first()

    if person.protected:
        abort(404)

    professional_details = (
        ProfessionalDetail.query.filter(ProfessionalDetail.person_id == person.id)
        .filter(ProfessionalDetail.end_date.is_(None))
        .all()
    )
    historical_professional_details = (
        ProfessionalDetail.query.filter(ProfessionalDetail.person_id == person.id)
        .filter(ProfessionalDetail.end_date.isnot(None))
        .all()
    )
    side_jobs = (
        SideJob.query.filter(SideJob.person_id == person.id)
        .filter(SideJob.end_date.is_(None))
        .all()
    )
    historical_side_jobs = (
        SideJob.query.filter(SideJob.person_id == person.id)
        .filter(SideJob.end_date.isnot(None))
        .all()
    )
    verdicts = (
        Verdict.query.join(Verdict.people)
        .filter(PersonVerdict.person_id == person.id)
        .order_by(Verdict.issued.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "person/detail.html",
        person=person,
        professional_details=professional_details,
        historical_professional_details=historical_professional_details,
        side_jobs=side_jobs,
        historical_side_jobs=historical_side_jobs,
        verdicts=verdicts,
    )
