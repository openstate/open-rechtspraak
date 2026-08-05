import uuid

from app.util import extract_initials, extract_titles, is_valid_uuid


def test_extract_titles():
    test_data = [
        {"name": "mr. O. Verhuis", "remaining_name": "O. Verhuis", "titles": ["mr."]},
        {"name": "W.G. Verlant", "remaining_name": "W.G. Verlant", "titles": []},
        {"name": "ing. W.G. Verlant", "remaining_name": "W.G. Verlant", "titles": ["ing."]},
        {"name": "W.G. Verlant MPA", "remaining_name": "W.G. Verlant", "titles": ["MPA"]},
        {"name": "mr. drs. H.A.G. Nijvrouw", "remaining_name": "H.A.G. Nijvrouw", "titles": ["mr.", "drs."]},
        {
            "name": "jonkheer mr. W. van Adel LL.M.",
            "remaining_name": "W. van Adel",
            "titles": ["jonkheer", "mr.", "LL.M."],
        },
        {"name": "prof. mr. F.J.L. Francken", "remaining_name": "F.J.L. Francken", "titles": ["prof.", "mr."]},
    ]

    for item in test_data:
        titles, remaining_name = extract_titles(item.get("name"))
        assert remaining_name == item.get("remaining_name")
        assert titles == item.get("titles")


def test_extract_initials():
    test_data = [
        {"name": "O. Verhuis", "remaining_name": "Verhuis", "initials": "O."},
        {"name": "W.G. Verlant", "remaining_name": "Verlant", "initials": "W.G."},
        {"name": "H.A.G. Nijvrouw", "remaining_name": "Nijvrouw", "initials": "H.A.G."},
        {"name": "W. van Adel", "remaining_name": "van Adel", "initials": "W."},
        {"name": "F.J.L. Francken", "remaining_name": "Francken", "initials": "F.J.L."},
    ]
    for item in test_data:
        initials, remaining_name = extract_initials(item.get("name"))
        assert remaining_name == item.get("remaining_name")
        assert initials == item.get("initials")


class TestIsValidUUID:
    def test_valid_uuid(self):
        id_ = str(uuid.uuid4())
        assert is_valid_uuid(id_) is True

    def test_invalid_uuid(self):
        id_ = "abc"
        assert is_valid_uuid(id_) is False
