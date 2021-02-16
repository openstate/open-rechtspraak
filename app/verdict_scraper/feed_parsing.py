from bs4 import BeautifulSoup


def to_soup(content):
    return BeautifulSoup(content, "lxml")


def extract_verdicts(soup):
    return soup.find_all("entry")


def safe_find_text(soup, selector):
    finding = soup.find(selector)
    if finding:
        return finding.text
