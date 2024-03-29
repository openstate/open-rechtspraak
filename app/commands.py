from datetime import datetime, timedelta

import click
from flask.cli import with_appcontext

from app.database import db
from app.scraper.other.institutions import import_institutions_handler
from app.scraper.other.legal_areas import import_legal_areas_handler
from app.scraper.other.procedure_types import import_procedure_types_handler
from app.scraper.people.enrich_people import enrich_people_handler
from app.scraper.people.import_people import import_people_handler
from app.scraper.verdicts.enrich_verdicts import enrich_verdicts_handler
from app.scraper.verdicts.import_verdicts import import_verdicts_handler


@click.command("import_people")
@with_appcontext
def import_people():
    import_people_handler()


@click.command("enrich_people")
@with_appcontext
def enrich_people():
    enrich_people_handler()


@click.command("import_verdicts")
@click.option("--start_date", default=None)
@click.option("--end_date", default=None)
@with_appcontext
def import_verdicts(start_date, end_date):
    if not start_date:
        start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    import_verdicts_handler(start_date, end_date)


@click.command("enrich_verdicts")
@with_appcontext
def enrich_verdicts():
    enrich_verdicts_handler()


@click.command("db_truncate")
@with_appcontext
def db_truncate():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print("Clear table %s" % table)
        db.session.execute(table.delete())
    db.session.commit()


@click.command("import_institutions")
@with_appcontext
def import_institutions():
    import_institutions_handler()


@click.command("import_procedure_types")
@with_appcontext
def import_procedure_types():
    import_procedure_types_handler()


@click.command("import_legal_areas")
@with_appcontext
def import_legal_areas():
    import_legal_areas_handler()
