from flask import Blueprint, render_template

from app.models import People

base_bp = Blueprint("base", __name__)


@base_bp.route("/")
def index():
    People.query.all()
    return render_template("index.html")

@base_bp.route("/about")
def about():
    return render_template("about.html")
