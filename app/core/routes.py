from flask import Blueprint, abort, redirect, render_template, url_for

from app.extensions import sitemap
from app.models import Person, PersonVerdict, ProfessionalDetail, SideJob, Verdict
from app.scraper.soup_parsing import find_beslissing, to_soup
from app.util import is_valid_uuid

core_bp = Blueprint("base", __name__)


@core_bp.route("/")
def index():
    return render_template("pages/index.html")


@core_bp.route("/about")
def about():
    return render_template("pages/about.html")


@core_bp.route("/api_docs")
def api_docs():
    person = Person.query.first()
    return render_template("pages/api_docs.html", person=person)


@core_bp.route("/verdict/<id>")
def verdict_detail(id):
    verdict = Verdict.query.filter(Verdict.id == id).first()
    beslissing = find_beslissing(to_soup(verdict.raw_xml))
    related_people = (
        Person.query.join(Person.verdicts)
        .filter(PersonVerdict.verdict_id == verdict.id)
        .filter(Person.protected.isnot(True))
        .all()
    )
    return render_template(
        "verdicts/detail.html",
        verdict=verdict,
        beslissing=beslissing,
        related_people=related_people,
    )


@core_bp.route("/verdict/ecli/<ecli>")
def verdict_by_ecli(ecli):
    verdict = Verdict.query.filter(Verdict.ecli == ecli).first()
    return verdict_detail(verdict.id)


@core_bp.route("/person/<id>")
def person_detail(id):
    if not is_valid_uuid(id):
        abort(404)

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


@core_bp.get("/rechtspraak/persoon/<slug>")
def redirect_from_old_paths(slug):
    slug = slug.replace("+", " ")
    slug = slug.rstrip()

    person = Person.query.filter(Person.toon_naam == slug).first()

    if person:
        return redirect(url_for("base.person_detail", id=person.id), code=301)
    else:
        return redirect(url_for("base.index", no_match=True), code=301)


@sitemap.register_generator
def post_blog():
    yield "base.index", {}, "", "daily", 1.0
    yield "base.about", {}, "", "weekly", 1.0

    for person in (
        Person.query.filter(Person.protected.isnot(True))
        .order_by(Person.last_scraped_at.desc())
        .all()
    ):
        yield "base.person_detail", {
            "id": person.id
        }, person.last_scraped_at, "weekly", 0.9
