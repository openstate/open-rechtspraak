import random
import string

from bs4 import BeautifulSoup

from app.models import ProfessionalDetails, SideJobs


def search_strings():
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
        ProfessionalDetails.query.filter(ProfessionalDetails.person_id == person.id)
        .filter(ProfessionalDetails.function == pd_kwargs.get("function"))
        .filter(ProfessionalDetails.organisation == pd_kwargs.get("organisation"))
        .filter(ProfessionalDetails.start_date == pd_kwargs.get("start_date"))
        .filter(ProfessionalDetails.end_date == pd_kwargs.get("end_date"))
        .all()
    )

    if professional_details:
        return True


def side_job_already_exists(person, nb_kwargs):
    side_jobs = (
        SideJobs.query.filter(SideJobs.person_id == person.id)
        .filter(SideJobs.function == nb_kwargs.get("function"))
        .filter(SideJobs.organisation_name == nb_kwargs.get("organisation_name"))
        .filter(SideJobs.organisation_type == nb_kwargs.get("organisation_type"))
        .filter(SideJobs.place == nb_kwargs.get("place"))
        .filter(SideJobs.start_date == nb_kwargs.get("start_date"))
        .filter(SideJobs.end_date == nb_kwargs.get("end_date"))
        .filter(SideJobs.paid == nb_kwargs.get("paid"))
        .all()
    )

    if side_jobs:
        return True
