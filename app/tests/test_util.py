import uuid

from app.util import is_valid_uuid


class TestIsValidUUID:
    def test_valid_uuid(self):
        id_ = str(uuid.uuid4())
        assert is_valid_uuid(id_) is True

    def test_invalid_uuid(self):
        id_ = "abc"
        assert is_valid_uuid(id_) is False
