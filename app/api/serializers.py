from datetime import datetime
from typing import Union

from app.models import Person, ProfessionalDetail, Verdict


def serialize_dt(dt: datetime) -> Union[str, None]:
    return dt.isoformat() if dt else None


def person_list_serializer(person: Person):
    professional_details = ProfessionalDetail.query.filter(
        ProfessionalDetail.person_id == person.id
    ).filter(ProfessionalDetail.end_date.is_(None))
    return {
        "id": person.id,
        "titles": person.titles,
        "initials": person.initials,
        "first_name": person.first_name,
        "last_name": person.last_name,
        "gender": person.gender,
        "toon_naam": person.toon_naam,
        "toon_naam_kort": person.toon_naam_kort,
        "rechtspraak_id": person.rechtspraak_id,
        "removed_from_rechtspraak_at": serialize_dt(person.removed_from_rechtspraak_at),
        "professional_details": [
            {
                "id": pd.id,
                "function": pd.function.title(),
                "organisation": pd.organisation,
            }
            for pd in professional_details
        ],
    }


def verdict_serializer(verdict: Verdict):
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
