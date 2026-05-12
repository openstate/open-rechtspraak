from datetime import datetime, timedelta

from app.models import Person


class TestPerson:
    def test_first_scraped_at_is_set_on_creation(self, person):
        assert person.first_scraped_at is not None
        assert isinstance(person.first_scraped_at, datetime)

    def test_first_scraped_at_is_set_to_current_datetime(self, person):
        one_second_ago = datetime.now() - timedelta(seconds=1)
        assert person.first_scraped_at >= one_second_ago

        in_one_second = datetime.now() + timedelta(seconds=1)
        assert person.first_scraped_at <= in_one_second

    def test_rechtspraak_external_id_is_succesfully_extracted(self):
        ids = [
            ("Gdt0tdGIIuzw8KSh2gMpRWZbZSWiGKxR", "665b6525a218ac51"),
            ("5dw03zI8T6G2KSdAjiB3KmZbZSWiGKxR", "665b6525a218ac51"),
            ("36Kwhv2cTaPtkHp4IuuRvmZbZSWiGKxR", "665b6525a218ac51"),
            ("HkSJNxWvetDolZ_2HMHWimZbZSWiGKxR", "665b6525a218ac51"),
            ("XXXXXXXXXXXXXXXXXXXXXmZbZSWiGKxR", "665b6525a218ac51"),
            ("asdfasdfasdfsadfasdfamZbZSWiGKxR", "665b6525a218ac51"),
            ("L8ls0piIS4ywQ24-SE8BDnVV0IdpuJZA", "7555d08769b89640"),
        ]

        for id_, result in ids:
            assert Person.extract_rechtspraak_internal_id(id_) == result
