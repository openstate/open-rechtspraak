import pytest
from werkzeug.datastructures import MultiDict

from app.api.services import BaseService
from app.models import Person


def test_base_service_max_limit():
    limit = 200
    query_params = MultiDict([("limit", limit)])
    service = BaseService(query_params)

    assert service.limit != limit
    assert service.limit == service.MAX_LIMIT


def test_default_pagination():
    service = BaseService(MultiDict([]))
    service.apply_pagination()

    assert service.queryset._limit_clause.value == BaseService.DEFAULT_LIMIT
    assert service.queryset._offset_clause.value == BaseService.DEFAULT_OFFSET


def test_custom_page():
    limit = 13
    offset = 28

    service = BaseService(MultiDict([("limit", limit), ("offset", offset)]))
    service.apply_pagination()

    assert service.queryset._limit_clause.value == limit
    assert service.queryset._offset_clause.value == offset


def test_ordering_without_order_raises_error():
    service = BaseService(MultiDict())

    with pytest.raises(ValueError):
        service.apply_ordering()


def test_ordering_applies_order_on_queryset():
    service = BaseService(MultiDict(), order=[Person.id.asc()])

    assert len(service.queryset._order_by_clauses) == 0
    service.apply_ordering()
    assert len(service.queryset._order_by_clauses) == 1
