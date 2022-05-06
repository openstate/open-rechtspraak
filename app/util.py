import os
from datetime import datetime
from typing import Union

import pytz


def get_env_variable(name, default=None) -> str:
    try:
        return os.environ.get(name, default=default)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def remove_milliseconds_from_epoch(epoch):
    return int(epoch) // 1000


def parse_rechtspraak_datetime(dt: str) -> Union[datetime, None]:
    """
    datetimes from the Rechtspraak API are formatted like this: "/Date(1598911200000+0200)/"

    Weirdly enough, they are epochs with milliseconds _and_ a timezone. The epoch itself it no in UTC, but in
    Europe/Amsterdam (as indicated by the +0200 / +0100). That's bad design on the side of the API.

    To be able to save UTC timestamps in the database, we use these teps:
    1. Strip timezone and remove milliseconds
    2. Convert to datetime
    3. Treat the datetime as if it is UTC and localize it to Europe/Amsterdam (datetime object with tzinfo)
    4. Remove the tzinfo from the datetime object, giving us a 'correct' UTC datetime object
    """
    if len(dt) < 5:
        # length of the datetime string is too short, we can't parse it to a valid epoch epoch
        return

    # Strip timezone and remove milliseconds, convert to datetime
    epoch = dt[6:][:-7]  # strip /Date( and +0200) from the string, yields epoch with milliseconds
    epoch = remove_milliseconds_from_epoch(epoch)
    dt = datetime.fromtimestamp(epoch)

    # Treat the datetime as if it is UTC and localize it to Europe/Amsterdam (datetime object with tzinfo)
    dutch_timezone = pytz.timezone("Europe/Amsterdam")
    dt = dt.astimezone(dutch_timezone)

    # Remove the tzinfo from the datetime object, giving us a 'correct' UTC datetime object
    dt = dt.replace(tzinfo=None)
    return dt


def determine_gender(toonnaam):
    if "dhr." in toonnaam:
        return "male"
    elif "mw." in toonnaam:
        return "female"
    else:
        "other"


def extract_initials(toonnaam_kort):
    return toonnaam_kort.split()[0]
