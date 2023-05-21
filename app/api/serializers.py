from app.models import Person, ProfessionalDetail, Verdict


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
    return {
        "id": verdict.id,
        "ecli": verdict.ecli,
        "title": verdict.title,
        "summary": verdict.summary,
        "uri": verdict.uri,
        "issued": verdict.issued,
        "type": verdict.type,
        "coverage": verdict.coverage,
        "subject": verdict.subject,
        "spatial": verdict.spatial,
        "procedure": verdict.procedure,
        "institution": verdict.institution.lido_id if verdict.institution else None,
        "procedure_type": verdict.procedure_type.lido_id
        if verdict.procedure_type
        else None,
        "legal_area": verdict.legal_area.legal_area_lido_id
        if verdict.legal_area
        else None,
    }
