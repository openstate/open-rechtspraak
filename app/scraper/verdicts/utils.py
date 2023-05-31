from typing import List

from flask import current_app

from app.models import Person, PersonVerdict, Verdict


def verdict_already_exists(ecli: str) -> bool:
    verdicts = Verdict.query.filter(Verdict.ecli == ecli).all()
    return True if verdicts else False


def person_verdict_already_exists(pv: dict) -> bool:
    pv = (
        PersonVerdict.query.filter(PersonVerdict.person_id == pv.get("person_id"))
        .filter(PersonVerdict.verdict_id == pv.get("verdict_id"))
        .filter(PersonVerdict.role == pv.get("role"))
        .all()
    )
    return True if pv else False


def recognize_people(text: str, people: List[Person] = None) -> List[Person]:
    if not people:
        current_app.logger.debug("No people received, querying people table")
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
