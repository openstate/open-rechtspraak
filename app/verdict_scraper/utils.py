from app.models import Person, PersonVerdict, Verdict


def verdict_already_exists(verdict):
    verdicts = Verdict.query.filter(Verdict.ecli == verdict.get("ecli")).all()

    if verdicts:
        return True


def person_verdict_already_exists(pv):
    pv = (
        PersonVerdict.query.filter(PersonVerdict.person_id == pv.get("person_id"))
        .filter(PersonVerdict.verdict_id == pv.get("verdict_id"))
        .filter(PersonVerdict.role == pv.get("role"))
        .all()
    )
    if pv:
        return True


def recognize_people(text):
    people = Person.query.all()
    found = []
    for person in people:
        if person.toon_naam.lower() in text.lower():
            found.append(person)
        elif person.toon_naam_kort.lower() in text.lower():
            found.append(person)
    return found
