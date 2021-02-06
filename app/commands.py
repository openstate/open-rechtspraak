import click
from flask.cli import with_appcontext

from app.scraper.extract import collect_and_save_people


@click.command("placeholder")
@with_appcontext
def placeholder():
    print("Still here!")


@click.command("import_people")
@with_appcontext
def import_people():
    collect_and_save_people()
