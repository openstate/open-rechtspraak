import random
import string

from bs4 import BeautifulSoup

from app.models import ProfessionalDetail, SideJob


def search_strings():
    """
    :return: list of search strings, that's formatted like this: ['aa', 'ab', 'ac', 'ad' ... 'ba', 'bb', 'zz']
    """
    result_set = []
    for char in string.ascii_lowercase:
        for second_char in string.ascii_lowercase:
            result_set.append(char + second_char)

    random.shuffle(result_set)
    return result_set


def format_payload(search_string):
    return {
        "model": '{"instantieCode":[],"overige_instantie":[],"naam":"'
        + search_string
        + '"}'
    }


def find_request_verification_token(content):
    soup = BeautifulSoup(content, "html.parser")
    return soup.find("input", {"name": "__RequestVerificationToken"})["value"]


def professional_detail_already_exists(person, pd_kwargs):
    professional_details = (
        ProfessionalDetail.query.filter(ProfessionalDetail.person_id == person.id)
        .filter(ProfessionalDetail.function == pd_kwargs.get("function"))
        .filter(ProfessionalDetail.organisation == pd_kwargs.get("organisation"))
        .filter(ProfessionalDetail.start_date == pd_kwargs.get("start_date"))
        .filter(ProfessionalDetail.end_date == pd_kwargs.get("end_date"))
        .all()
    )

    if professional_details:
        return True


def side_job_already_exists(person, nb_kwargs):
    side_jobs = (
        SideJob.query.filter(SideJob.person_id == person.id)
        .filter(SideJob.function == nb_kwargs.get("function"))
        .filter(SideJob.organisation_name == nb_kwargs.get("organisation_name"))
        .filter(SideJob.organisation_type == nb_kwargs.get("organisation_type"))
        .filter(SideJob.place == nb_kwargs.get("place"))
        .filter(SideJob.start_date == nb_kwargs.get("start_date"))
        .filter(SideJob.end_date == nb_kwargs.get("end_date"))
        .filter(SideJob.paid == nb_kwargs.get("paid"))
        .all()
    )

    if side_jobs:
        return True
