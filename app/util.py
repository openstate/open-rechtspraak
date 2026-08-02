import os
from datetime import datetime
from uuid import UUID

import pytz

MIN_RECHTSPRAAK_DATETIME_LENGTH = 5

PREFIX_TITLES = ["jonkheer", "mr.", "dr.", "drs.", "prof.", "ing."]
SUFFIX_TITLES = ["LL.M.", "MPA"]


def get_env_variable(name: str, default: str | None = None) -> str:
    try:
        return os.environ.get(name, default=default)
    except KeyError:
        message = f"Expected environment variable '{name}' not set."
        raise OSError(message)


def remove_milliseconds_from_epoch(epoch: str) -> int:
    return int(epoch) // 1000


def parse_rechtspraak_datetime(dt: str) -> datetime | None:
    """Datetimes from the Rechtspraak API are formatted like this: "/Date(1598911200000+0200)/"

    Weirdly enough, they are epochs with milliseconds _and_ a timezone. The epoch itself it no in UTC, but in
    Europe/Amsterdam (as indicated by the +0200 / +0100). That's bad design on the side of the API.

    To be able to save UTC timestamps in the database, we use these teps:
    1. Strip timezone and remove milliseconds
    2. Convert to datetime
    3. Treat the datetime as if it is UTC and localize it to Europe/Amsterdam (datetime object with tzinfo)
    4. Remove the tzinfo from the datetime object, giving us a 'correct' UTC datetime object
    """
    if len(dt) < MIN_RECHTSPRAAK_DATETIME_LENGTH:
        # length of the datetime string is too short, we can't parse it to a valid epoch epoch
        return None

    # Strip timezone and remove milliseconds, convert to datetime
    # strips /Date( and +0200) from the string, yields epoch with milliseconds
    epoch = dt[6:][:-7]
    epoch = remove_milliseconds_from_epoch(epoch)
    dt = datetime.fromtimestamp(epoch)

    # Treat the datetime as if it is UTC and localize it to Europe/Amsterdam (datetime object with tzinfo)
    dutch_timezone = pytz.timezone("Europe/Amsterdam")
    dt = dt.astimezone(dutch_timezone)

    # Remove the tzinfo from the datetime object, giving us a 'correct' UTC datetime object
    return dt.replace(tzinfo=None)


def extract_initials(name: str) -> tuple[str, str]:
    """
    Returns a tuple with initials and the rest of the name"""
    return name.split(maxsplit=1)


def titles_left(name: str) -> bool:
    if any([name.startswith(title) for title in PREFIX_TITLES]):
        return True
    if any([name.endswith(title) for title in SUFFIX_TITLES]):
        return True
    return False


def extract_titles(name: str) -> tuple[str, list[str]]:
    titles = []

    while True:
        if not titles_left(name):
            break

        for title in PREFIX_TITLES:
            if name.startswith(title):
                name = name.replace(title, "").strip()
                titles.append(title)

        for title in SUFFIX_TITLES:
            if name.endswith(title):
                name = name.replace(title, "").strip()
                titles.append(title)

    return titles, name


def is_valid_uuid(uuid: str) -> bool:
    try:
        UUID(uuid, version=4)
    except ValueError:
        return False
    else:
        return True
