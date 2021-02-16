from app.models import Verdicts


def verdict_already_exists(verdict):
    verdicts = Verdicts.query.filter(Verdicts.ecli == verdict.get("ecli")).all()

    if verdicts:
        return True
