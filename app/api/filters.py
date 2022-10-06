from app.models import Person


class PersonFilterService:
    DEFAULT_LIMIT = 20
    MAX_LIMIT = 100
    DEFAULT_ORDER = Person.last_name.asc()

    def __init__(self, query_params):
        self.query = Person.query.filter(Person.protected.isnot(True))
        self.limit = self.parse_limit(
            query_params.get("limit", default=self.DEFAULT_LIMIT, type=int)
        )
        self.offset = query_params.get("offset", default=0, type=int)
        self.q = query_params.get("q", None)
        self.include_former_judges = query_params.get(
            "former_judges", default=False, type=bool
        )
        self.order = self.DEFAULT_ORDER

    def parse_limit(self, limit=DEFAULT_LIMIT):
        if limit > self.MAX_LIMIT:
            limit = self.MAX_LIMIT
        return limit

    def apply_filters(self):
        if self.q:
            self.query = self.query.filter(Person.toon_naam.ilike(f"%{self.q}%"))

        if self.include_former_judges is False:
            self.query = self.query.filter(Person.removed_from_rechtspraak_at.is_(None))

        self.query = self.query.order_by(self.order)

    def apply_pagination(self):
        self.query = self.query.limit(self.limit)
        self.query = self.query.offset(self.offset)
