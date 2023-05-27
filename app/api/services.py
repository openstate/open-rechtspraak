from sqlalchemy.orm import Query, joinedload
from werkzeug.datastructures import MultiDict

from app.models import Person, PersonVerdict, Verdict


class BaseService:
    DEFAULT_OFFSET = 0
    DEFAULT_LIMIT = 20
    MAX_LIMIT = 100

    def __init__(
        self, query_params: MultiDict, queryset: Query = None, order: list = None
    ):
        self.limit = self._max_limit(
            query_params.get("limit", default=self.DEFAULT_LIMIT, type=int)
        )
        self.offset = query_params.get("offset", default=self.DEFAULT_OFFSET, type=int)
        self.queryset = queryset or Query([])
        self.order = order or []

    def _max_limit(self, limit: int):
        if limit > self.MAX_LIMIT:
            limit = self.MAX_LIMIT
        return limit

    def apply_ordering(self):
        if len(self.order) == 0:
            raise ValueError(
                "You did not specify any attributes to order the queryset on."
            )

        for order in self.order:
            self.queryset = self.queryset.order_by(order)
        return self.queryset

    def apply_pagination(self):
        self.queryset = self.queryset.limit(self.limit)
        self.queryset = self.queryset.offset(self.offset)
        return self.queryset


class PersonService(BaseService):
    def __init__(self, query_params=MultiDict[str, str]):
        super().__init__(query_params)
        self.query_params = query_params
        self.queryset = Person.query.filter(Person.protected.isnot(True))
        self.order = [Person.last_name.asc(), Person.id.asc()]

    def list_query(self, query_params):
        q = query_params.get("q", None)
        if q:
            self.queryset = self.queryset.filter(Person.toon_naam.ilike(f"%{q}%"))

        include_former_judges = query_params.get(
            "former_judges", default=False, type=bool
        )
        if include_former_judges is False:
            self.queryset = self.queryset.filter(
                Person.removed_from_rechtspraak_at.is_(None)
            )

        self.queryset = self.apply_ordering()
        self.queryset = self.queryset.limit(self.limit)
        self.queryset = self.queryset.offset(self.offset)
        return self.queryset


class PersonVerdictsService(BaseService):
    def __init__(self, person: Person, query_params=MultiDict[str, str]):
        super().__init__(query_params)
        self.query_params = query_params
        self.queryset = (
            Verdict.query.join(Verdict.people)
            .options(joinedload(Verdict.legal_area))
            .options(joinedload(Verdict.institution))
            .options(joinedload(Verdict.procedure_type))
            .filter(PersonVerdict.person_id == person.id)
        )
        self.order = [Verdict.issued.desc(), Verdict.id.asc()]

    def list_query(self):
        self.queryset = self.apply_ordering()
        self.queryset = self.queryset.limit(self.limit)
        self.queryset = self.queryset.offset(self.offset)
        return self.queryset
