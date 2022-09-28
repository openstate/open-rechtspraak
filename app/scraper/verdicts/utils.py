from flask import current_app

from app.models import Person, PersonVerdict, Verdict


def verdict_already_exists(ecli):
    verdicts = Verdict.query.filter(Verdict.ecli == ecli).all()

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


def recognize_people(text, people=None):
    if not people:
        current_app.logger.info("No people received, querying people table")
        people = Person.query.all()

    found = []
    text = text.lower()
    for person in people:
        name = person.toon_naam.lower()
        if name in text:
            found.append(person)
            continue

        short_name = person.toon_naam_kort.lower()
        if short_name in text:
            found.append(person)
            continue
    return found
