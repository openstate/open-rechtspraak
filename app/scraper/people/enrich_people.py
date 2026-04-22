from datetime import datetime

from flask import current_app

from app.models import Person, ProfessionalDetail, SideJob
from app.scraper.people.config import DETAILS_ENDPOINT, FAULTY_URL
from app.scraper.people.utils import (
    find_institution_for_professional_detail,
    professional_detail_already_exists,
    side_job_already_exists,
)
from app.scraper.rechtspraak_session import RechtspraakScrapeSession


def enrich_people_handler():
    people = Person.query.all()

    # Rate limit to default requests p/s, which means that enriching 5.000 judges will take a little less than 3 hours
    with RechtspraakScrapeSession() as session:
        for person in people:
            enrich_person(session, person)


def person_details_url(rechtspraak_id: str) -> str:
    return DETAILS_ENDPOINT + rechtspraak_id


def enrich_person(session: RechtspraakScrapeSession, person: Person) -> None:
    r = session.get(person_details_url(person.rechtspraak_id))
    current_app.logger.info(
        f"Enriching person {person.id} with information from {r.url}"
    )

    # r.ok means a status code of 400 or higher 
    # FAULTY_URL means we were redirected to FAULTY_URL
    # if no "model" key exists, it means the person does not exist anymore in namenlijst
    if not r.ok or r.url == FAULTY_URL or not r.json().get("model"):
        current_app.logger.warning(
            f"Enrichtment of person {person.id} failed with status {r.status_code}, url {r.url}",
            extra={"id": person.id},
        )
        person.removed_from_rechtspraak_at = datetime.now()
        person.last_scraped_at = datetime.now()
        person.save()
        return

    person_json = r.json().get("model", {})

    for beroepsgegeven in person_json.get("beroepsgegevens", []):
        pd_kwargs = ProfessionalDetail.transform_beroepsgegevens_dict(
            beroepsgegeven
        )
        if not professional_detail_already_exists(person, pd_kwargs):
            institution = find_institution_for_professional_detail(
                pd_kwargs.get("organisation")
            )
            ProfessionalDetail.create(
                **{"person_id": person.id, **pd_kwargs}, institution=institution
            )

    for historisch_beroepsgegeven in person_json.get("historieBeroepsgegevens", []):
        pd_kwargs = ProfessionalDetail.transform_historisch_beroepsgegevens_dict(
            historisch_beroepsgegeven
        )
        if not professional_detail_already_exists(person, pd_kwargs):
            institution = find_institution_for_professional_detail(
                pd_kwargs.get("organisation")
            )
            ProfessionalDetail.create(
                **{"person_id": person.id, **pd_kwargs}, institution=institution
            )

    for nevenbetrekking in person_json.get("huidigeNevenbetrekkingen", []):
        nb_kwargs = SideJob.transform_huidige_nevenbetrekkingen_dict(
            nevenbetrekking
        )
        if not side_job_already_exists(person, nb_kwargs):
            SideJob.create(**{"person_id": person.id, **nb_kwargs})

    for voorgaande_nevenbetrekking in person_json.get(
        "voorgaandeNevenbetrekkingen", []
    ):
        nb_kwargs = SideJob.transform_voorgaande_nevenbetrekkingen_dict(
            voorgaande_nevenbetrekking
        )
        if not side_job_already_exists(person, nb_kwargs):
            SideJob.create(**{"person_id": person.id, **nb_kwargs})

    person.removed_from_rechtspraak_at = None
    person.last_scraped_at = datetime.now()
    person.save()
