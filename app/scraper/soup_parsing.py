from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from bs4._typing import _StrainableAttributes


def to_soup(content: str, features: str = "xml") -> BeautifulSoup:
    """Uses the 'xml' parser by default. If you are converting html documents, use 'html.parser'."""
    return BeautifulSoup(content, features=features)


def extract_rnl_state(soup: BeautifulSoup) -> BeautifulSoup:
    return soup.find(id="rnl-state")


def extract_verdicts(soup: BeautifulSoup) -> BeautifulSoup:
    return soup.find_all("entry")


def safe_find_text(soup: BeautifulSoup, selector: str, attrs: _StrainableAttributes | None = None) -> str:
    finding = soup.find(selector, attrs=attrs)
    return finding.text if finding else ""


def find_elements_containing(soup: BeautifulSoup, text: str) -> list:
    sections = soup.find_all("section")
    result = []
    for section in sections:
        for word in text:
            if word in section.text:
                result.append(section.text)
                continue
    return result


def find_beslissing(soup: BeautifulSoup) -> str:
    beslissings_text = ""
    beslissings_text += safe_find_text(soup, "section", {"role": "beslissing"})
    results = find_elements_containing(
        soup,
        [
            "rechter",
            "voorzitter",
            "griffier",
            "griffiers",
            "Dit vonnis is gewezen door",
            "raadsheren",
            "Aldus gegeven door",
        ],
    )
    beslissings_text += " ".join(results)

    if not beslissings_text:
        beslissings_text = safe_find_text(soup, "uitspraak")

    return beslissings_text


def find_institution_identifier(soup: BeautifulSoup) -> str:
    creator = soup.find("dcterms:creator")
    if creator:
        identifier = creator.get("resourceidentifier")
        if not identifier:
            identifier = creator.get("psi:resourceIdentifier")
        return identifier
    return ""


def find_procedure_type_identifier(soup: BeautifulSoup) -> str:
    procedure_type = soup.find("psi:procedure")
    return procedure_type.get("resourceIdentifier") if procedure_type else ""


def find_legal_area_identifier(soup: BeautifulSoup) -> str:
    legal_area = soup.find("dcterms:subject")
    return legal_area.get("resourceIdentifier") if legal_area else ""
