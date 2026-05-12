from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Person, ProfessionalDetail, Verdict


def serialize_dt(dt: datetime) -> str | None:
    return dt.isoformat() if dt else None


def professional_detail_serializer(pd: ProfessionalDetail) -> dict:
    return {
        "id": pd.id,
        "function": pd.function.title(),
        "organisation": pd.organisation,
        "main_job": pd.main_job,
        "remarks": pd.remarks,
        "location": pd.location,
        "outside_of_judiciary": pd.outside_of_judiciary,
        "start_date": pd.start_date.isoformat() if pd.start_date else None,
        "end_date": pd.end_date.isoformat() if pd.end_date else None,
    }


def person_list_serializer(person: Person) -> dict:
    # return all professional details, ordered from newest to oldest
    professional_details = sorted(
        person.professional_detail, key=lambda r: r.start_date if r.start_date else datetime(1970, 1, 1), reverse=True
    )

    return {
        "id": person.id,
        "titles": person.titles,
        "initials": person.initials,
        "last_name": person.last_name,
        "last_name_own": person.last_name_own,
        "last_name_partner": person.last_name_partner,
        "did_not_self_report_side_jobs": person.did_not_self_report_side_jobs,
        "has_no_side_jobs": person.has_no_side_jobs,
        "gender": person.gender,
        "toon_naam": person.toon_naam,
        "toon_naam_kort": person.toon_naam_kort,
        "rechtspraak_id": person.rechtspraak_id,
        "rechtspraak_internal_id": person.rechtspraak_internal_id,
        "removed_from_rechtspraak_at": serialize_dt(person.removed_from_rechtspraak_at),
        "professional_details": [professional_detail_serializer(pd) for pd in professional_details],
    }


def verdict_serializer(verdict: Verdict) -> dict:
    procedure_type = verdict.procedure_type.lido_id if verdict.procedure_type else None
    legal_area = verdict.legal_area.legal_area_lido_id if verdict.legal_area else None
    institution = verdict.institution.lido_id if verdict.institution else None
    return {
        "id": verdict.id,
        "ecli": verdict.ecli,
        "title": verdict.title,
        "summary": verdict.summary,
        "uri": verdict.uri,
        "issued": serialize_dt(verdict.issued),
        "type": verdict.type,
        "coverage": verdict.coverage,
        "subject": verdict.subject,
        "spatial": verdict.spatial,
        "procedure": verdict.procedure,
        "institution": institution,
        "procedure_type": procedure_type,
        "legal_area": legal_area,
    }
