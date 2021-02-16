from bs4 import BeautifulSoup


def to_soup(content):
    return BeautifulSoup(content, "lxml")


def extract_verdicts(soup):
    return soup.find_all("entry")


def safe_find_text(soup, selector, attrs=None):
    finding = soup.find(selector, attrs=attrs)
    if finding:
        return finding.text
    else:
        return ""


def find_elements_containing(soup, text):
    sections = soup.find_all("section")
    result = []
    for section in sections:
        for word in text:
            if word in section.text:
                result.append(section.text)
                continue
    return result


def find_beslissing(soup):
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