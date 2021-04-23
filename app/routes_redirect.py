from flask import Blueprint, redirect

redirect_bp = Blueprint("redirect", __name__, url_prefix="/redirect")


@redirect_bp.route("/rechtspraak/open-data")
def rechtspraak_open_data():
    return redirect("https://www.rechtspraak.nl/Uitspraken/paginas/open-data.aspx")


@redirect_bp.route("/rechtspraak/search")
def rechtspraak_search():
    return redirect("https://namenlijst.rechtspraak.nl/")


@redirect_bp.route("/rechtspraak/persoon/<id>")
def rechtspraak_persoon(id):
    return redirect(f"https://namenlijst.rechtspraak.nl/#!/details/{id}")


@redirect_bp.route("/rechtspraak/uitspraak/<ecli>")
def rechtspraak_uitspraak(ecli):
    return redirect(f"https://uitspraken.rechtspraak.nl/InzienDocument?id={ecli}")
