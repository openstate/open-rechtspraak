from datetime import datetime, timedelta
from operator import or_

from flask import current_app, json

from app.models import Person, ProfessionalDetail, SideJob
from app.scraper.people.config import DETAILS_ENDPOINT
from app.scraper.people.utils import (
    find_institution_for_professional_detail,
    professional_detail_already_exists,
    side_job_already_exists,
)
from app.scraper.rechtspraak_session import RechtspraakScrapeSession
from app.scraper.soup_parsing import extract_rnl_state, to_soup

RESCRAPE_AFTER_HOURS = 20


def people_to_enrich() -> list[Person]:
    """Yield people that should be enriched.

    People that should be enriched have either:
     - not been scraped in the past RESCRAPE_AFTER_HOURS hours, or
     - have never been scraped before.
    """
    rescrape_after = datetime.now() - timedelta(hours=RESCRAPE_AFTER_HOURS)
    return Person.query.filter(or_(Person.last_scraped_at <= rescrape_after, Person.last_scraped_at.is_(None))).all()


def enrich_people_handler() -> None:
    """Enriches all known people"""
    people = people_to_enrich()
    current_app.logger.info(
        f"Enriching {len(people)} people that weren't enriched in the past {RESCRAPE_AFTER_HOURS} hours",
    )

    # Rate limit to default requests p/s, which means that enriching 5.000 judges will take a little less than 3 hours
    with RechtspraakScrapeSession() as session:
        for person in people:
            enrich_person(session, person)


def enrich_person_handler(person_id: str) -> None:
    """Enriches a single person by their id."""
    person = Person.query.filter(Person.id == person_id).first()

    if not person:
        raise ValueError(f"person with id '{person_id}' does not exist")

    with RechtspraakScrapeSession() as session:
        enrich_person(session, person)


def person_details_url(rechtspraak_id: str) -> str:
    """Yield the publicly accessible url for a person to scrape."""
    return DETAILS_ENDPOINT + rechtspraak_id


def enrich_person(session: RechtspraakScrapeSession, person: Person) -> None:  # noqa: PLR0912
    """Enrich a single person"""
    r = session.get(person_details_url(person.rechtspraak_id))
    current_app.logger.info(f"Enriching person {person.id} with information from {r.url}")

    if not r.ok:
        current_app.logger.warning(
            f"Enrichment of person {person.id} failed with status {r.status_code}, url {r.url}",
            extra={"id": person.id},
        )
        person.removed_from_rechtspraak_at = datetime.now()
        person.last_scraped_at = datetime.now()
        person.save()
        return

    soup = to_soup(r.content, features="html.parser")
    state = extract_rnl_state(soup).text
    person_json = json.loads(state).get("neroRechterlijkeAmbtenaarDetails")

    # This indicates that the person did exist in, but does not exist
    # anymore. This means that the person has been removed from the register.
    if not person_json:
        current_app.logger.warning(f"Person '{person.id}' has been removed")
        person.removed_from_rechtspraak_at = datetime.now()
        person.last_scraped_at = datetime.now()
        person.save()
        return

    for beroepsgegeven in person_json.get("actieveBeroepsgegevens", []):
        pd_kwargs = ProfessionalDetail.transform_beroepsgegevens_dict(beroepsgegeven)
        if not professional_detail_already_exists(person, pd_kwargs):
            institution = find_institution_for_professional_detail(pd_kwargs.get("organisation"))
            ProfessionalDetail.create(**{"person_id": person.id, **pd_kwargs}, institution=institution)

    for historisch_beroepsgegeven in person_json.get("historieBeroepsgegevens", []):
        pd_kwargs = ProfessionalDetail.transform_historisch_beroepsgegevens_dict(historisch_beroepsgegeven)
        if not professional_detail_already_exists(person, pd_kwargs):
            institution = find_institution_for_professional_detail(pd_kwargs.get("organisation"))
            ProfessionalDetail.create(**{"person_id": person.id, **pd_kwargs}, institution=institution)

    for voorgaande_betrekking in person_json.get("voorgaandeBetrekkingen", []):
        pd_kwargs = ProfessionalDetail.transform_voorgaande_betrekking_dict(voorgaande_betrekking)
        if not professional_detail_already_exists(person, pd_kwargs):
            institution = find_institution_for_professional_detail(pd_kwargs.get("organisation"))
            ProfessionalDetail.create(**{"person_id": person.id, **pd_kwargs}, institution=institution)

    for beroepsgegeven in person_json.get("beroepsgegevensBuitenRM", []):
        pd_kwargs = ProfessionalDetail.transform_beroepsgegevens_buiten_rm_dict(beroepsgegeven)
        if not professional_detail_already_exists(person, pd_kwargs):
            institution = find_institution_for_professional_detail(pd_kwargs.get("organisation"))
            ProfessionalDetail.create(**{"person_id": person.id, **pd_kwargs}, institution=institution)

    for nevenbetrekking in person_json.get("huidigeNevenbetrekkingen", []):
        nevenbetrekking_kwargs = SideJob.transform_huidige_nevenbetrekkingen_dict(nevenbetrekking)
        if not side_job_already_exists(person, nevenbetrekking_kwargs):
            SideJob.create(**{"person_id": person.id, **nevenbetrekking_kwargs})

    for voorgaande_nevenbetrekking in person_json.get("voorgaandeNevenbetrekkingen", []):
        nevenbetrekking_kwargs = SideJob.transform_voorgaande_nevenbetrekkingen_dict(voorgaande_nevenbetrekking)
        if not side_job_already_exists(person, nevenbetrekking_kwargs):
            SideJob.create(**{"person_id": person.id, **nevenbetrekking_kwargs})

    person.did_not_self_report_side_jobs = person_json.get("geenOpgaveNevenbetrekkingen")
    person.has_no_side_jobs = person_json.get("vervultGeenNevenbetrekkingen")
    person.removed_from_rechtspraak_at = None
    person.last_scraped_at = datetime.now()
    person.save()
