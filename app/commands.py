import click
from flask.cli import with_appcontext


@click.command("placeholder")
@with_appcontext
def placeholder():
    print("Still here!")
