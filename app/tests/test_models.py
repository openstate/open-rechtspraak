from datetime import datetime, timedelta


class TestPerson:
    def test_first_scraped_at_is_set_on_creation(self, person):
        assert person.first_scraped_at is not None
        assert isinstance(person.first_scraped_at, datetime)

    def test_first_scraped_at_is_set_to_current_datetime(self, person):
        one_second_ago = datetime.now() - timedelta(seconds=1)
        assert person.first_scraped_at >= one_second_ago

        in_one_second = datetime.now() + timedelta(seconds=1)
        assert person.first_scraped_at <= in_one_second
