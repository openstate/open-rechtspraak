import string


def search_strings():
    result_set = []
    for char in string.ascii_lowercase:
        for second_char in string.ascii_lowercase:
            result_set.append(char + second_char)

    return result_set


def format_payload(search_string):
    return {
        "model": '{"instantieCode":[],"overige_instantie":[],"naam":"'
        + search_string
        + '"}'
    }
