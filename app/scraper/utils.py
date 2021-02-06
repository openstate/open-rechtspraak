import random
import string

from bs4 import BeautifulSoup


def search_strings():
    result_set = []
    for char in string.ascii_lowercase:
        for second_char in string.ascii_lowercase:
            result_set.append(char + second_char)

    random.shuffle(result_set)
    return result_set


def format_payload(search_string):
    return {
        "model": '{"instantieCode":[],"overige_instantie":[],"naam":"'
        + search_string
        + '"}'
    }


def find_request_verification_token(content):
    soup = BeautifulSoup(content, "html.parser")
    return soup.find("input", {"name": "__RequestVerificationToken"})["value"]
