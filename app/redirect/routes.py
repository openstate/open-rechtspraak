from flask import Blueprint, Response, redirect

redirect_bp = Blueprint("redirect", __name__, url_prefix="/redirect")


@redirect_bp.route("/rechtspraak/open-data")
def rechtspraak_open_data() -> Response:
    return redirect("https://www.rechtspraak.nl/Uitspraken/paginas/open-data.aspx")


@redirect_bp.route("/rechtspraak/search")
def rechtspraak_search() -> Response:
    return redirect("https://www.rechtspraak.nl/registers/nevenfunctieregister")


@redirect_bp.route("/rechtspraak/persoon/<id>")
def rechtspraak_persoon(id: str) -> Response:
    return redirect(f"https://www.rechtspraak.nl/registers/nevenfunctieregister/details/{id}")


@redirect_bp.route("/rechtspraak/uitspraak/<ecli>")
def rechtspraak_uitspraak(ecli: str) -> Response:
    return redirect(f"https://uitspraken.rechtspraak.nl/InzienDocument?id={ecli}")
