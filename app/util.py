import os
from datetime import datetime
from uuid import UUID

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
    """Datetimes from the Rechtspraak API are formatted like this: "2020-01-01" """
    if not dt:
        return None
    return datetime.strptime(dt, "%Y-%m-%d")


def extract_initials(name: str) -> tuple[str, str]:
    """
    Returns a tuple with initials and the rest of the name.
    MUST be run on a name without titles. Use the extract_titles function first."""
    return name.split(maxsplit=1)


def titles_left(name: str) -> bool:
    if any([name.startswith(title) for title in PREFIX_TITLES]):
        return True
    if any([name.endswith(title) for title in SUFFIX_TITLES]):
        return True
    return False


def extract_titles(name: str) -> tuple[str, list[str]]:
    titles = []
    remaining_name = name

    while True:
        if not titles_left(remaining_name):
            break

        for title in PREFIX_TITLES:
            if remaining_name.startswith(title):
                remaining_name = remaining_name.replace(title, "").strip()
                titles.append(title)

        for title in SUFFIX_TITLES:
            if remaining_name.endswith(title):
                remaining_name = remaining_name.replace(title, "").strip()
                titles.append(title)

    return titles, remaining_name


def is_valid_uuid(uuid: str) -> bool:
    try:
        UUID(uuid, version=4)
    except ValueError:
        return False
    else:
        return True
