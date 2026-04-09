from flask_mongo_drf.mongo_paginations import MongoPagination


def test_pagination_basic():
    args = {"page": "2", "page_size": "5"}
    paginator = MongoPagination(args, count=20, endpoint_name="test")

    assert paginator.page_number == 2
    assert paginator.limit == 5
    assert paginator.skip == 5


def test_pagination_meta():
    args = {"page": "1", "page_size": "10"}
    paginator = MongoPagination(args, count=25, endpoint_name="test")

    meta = paginator.get_meta()
    assert meta["total_pages"] == 3