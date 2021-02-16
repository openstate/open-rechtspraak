from app.models import Verdict


def verdict_already_exists(verdict):
    verdicts = Verdict.query.filter(Verdict.ecli == verdict.get("ecli")).all()

    if verdicts:
        return True
