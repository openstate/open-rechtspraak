from app.models import Person, ProfessionalDetail


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
