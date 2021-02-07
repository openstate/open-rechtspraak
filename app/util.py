import os
from datetime import datetime


def get_env_variable(name, default=None) -> str:
    try:
        return os.environ.get(name, default=default)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def strip_rechtspraak_datetime(dt):
    return dt[6:][:-7]


def rechtspraak_to_epoch(dt):
    return int(dt) / 1000


def parse_rechtspraak_datetime(dt):
    if len(dt) < 5:
        return
    epoch = rechtspraak_to_epoch(strip_rechtspraak_datetime(dt))
    return datetime.fromtimestamp(epoch)


def determine_gender(toonnaam):
    if "dhr." in toonnaam:
        return "male"
    elif "mw." in toonnaam:
        return "female"
    else:
        "other"


def extract_initials(toonnaam_kort):
    return toonnaam_kort.split()[0]
