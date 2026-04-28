import random
import string

from bs4 import BeautifulSoup

from app.models import Institution, Person, ProfessionalDetail, SideJob


def search_strings() -> list[str]:
    """:return: list of search strings, that's formatted like this: ['aa', 'ab', 'ac', 'ad' ... 'ba', 'bb', 'zz']"""
    result_set = []
    for first in string.ascii_lowercase:
        for second in string.ascii_lowercase:
            search_string = first + second
            result_set.append(search_string)

    random.shuffle(result_set)
    return result_set


def format_payload(search_string: str) -> dict:
    return {"model": '{"instantieCode":[],"overige_instantie":[],"naam":"' + search_string + '"}'}


def find_request_verification_token(content: str) -> str | None:
    soup = BeautifulSoup(content, "html.parser")
    return soup.find("input", {"name": "__RequestVerificationToken"})["value"]


def professional_detail_already_exists(person: Person, professional_detail_kwargs: dict) -> bool:
    professional_details = (
        ProfessionalDetail.query.filter(ProfessionalDetail.person_id == person.id)
        .filter(ProfessionalDetail.function == professional_detail_kwargs.get("function"))
        .filter(ProfessionalDetail.organisation == professional_detail_kwargs.get("organisation"))
        .filter(ProfessionalDetail.start_date == professional_detail_kwargs.get("start_date"))
        .filter(ProfessionalDetail.end_date == professional_detail_kwargs.get("end_date"))
        .all()
    )

    return True if professional_details else False


def side_job_already_exists(person: Person, nevenbetrekking_kwargs: dict) -> bool:
    side_jobs = (
        SideJob.query.filter(SideJob.person_id == person.id)
        .filter(SideJob.function == nevenbetrekking_kwargs.get("function"))
        .filter(SideJob.organisation_name == nevenbetrekking_kwargs.get("organisation_name"))
        .filter(SideJob.organisation_type == nevenbetrekking_kwargs.get("organisation_type"))
        .filter(SideJob.place == nevenbetrekking_kwargs.get("place"))
        .filter(SideJob.start_date == nevenbetrekking_kwargs.get("start_date"))
        .filter(SideJob.end_date == nevenbetrekking_kwargs.get("end_date"))
        .filter(SideJob.paid == nevenbetrekking_kwargs.get("paid"))
        .all()
    )

    return True if side_jobs else False


def find_institution_for_professional_detail(institution: Institution) -> Institution:
    return Institution.query.filter(Institution.name.ilike(institution)).first()
