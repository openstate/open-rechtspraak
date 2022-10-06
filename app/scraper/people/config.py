SEARCH_ENDPOINT = "https://namenlijst.rechtspraak.nl/Services/WebNamenlijstService/Zoek"
DETAILS_ENDPOINT = (
    "https://namenlijst.rechtspraak.nl/Services/WebNamenlijstService/haalOp/?id="
)

HEADERS = {
    "Referer": "https://namenlijst.rechtspraak.nl/",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8",
}
