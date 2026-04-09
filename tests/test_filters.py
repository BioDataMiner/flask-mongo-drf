import pytest
from flask_mongo_rest.mongo_filters import FilterSet, CharFilter, NumberFilter, BooleanFilter


class UserFilterSet(FilterSet):
    """Example FilterSet for testing"""
    username = CharFilter(lookup_expr='icontains')
    email = CharFilter(lookup_expr='exact')
    age = NumberFilter(lookup_expr='gte')
    is_active = BooleanFilter()


class TestFilterSet:
    """Test suite for FilterSet and Filter classes"""

    def test_char_filter_icontains(self):
        """Test CharFilter with icontains lookup"""
        filter_set = UserFilterSet(data={"username": "john"})
        query = filter_set.get_query_dict()
        assert "username" in query
        assert "$regex" in query["username"]

    def test_char_filter_exact(self):
        """Test CharFilter with exact lookup"""
        filter_set = UserFilterSet(data={"email": "john@example.com"})
        query = filter_set.get_query_dict()
        assert query.get("email") == "john@example.com"

    def test_number_filter_gte(self):
        """Test NumberFilter with gte (greater than or equal) lookup"""
        filter_set = UserFilterSet(data={"age": "30"})
        query = filter_set.get_query_dict()
        assert "age" in query
        assert "$gte" in query["age"]

    def test_boolean_filter(self):
        """Test BooleanFilter"""
        filter_set = UserFilterSet(data={"is_active": "true"})
        query = filter_set.get_query_dict()
        assert query.get("is_active") is True

    def test_multiple_filters(self):
        """Test multiple filters combined"""
        filter_set = UserFilterSet(data={
            "username": "john",
            "age": "25",
            "is_active": "true"
        })
        query = filter_set.get_query_dict()
        assert "username" in query
        assert "age" in query
        assert "is_active" in query

    def test_empty_filter(self):
        """Test FilterSet with no data"""
        filter_set = UserFilterSet(data={})
        query = filter_set.get_query_dict()
        assert query == {}

    def test_invalid_number_filter(self):
        """Test NumberFilter with invalid number"""
        filter_set = UserFilterSet(data={"age": "invalid"})
        # Should handle gracefully or skip invalid values
        query = filter_set.get_query_dict()
        # Behavior depends on implementation

    def test_filter_declared_fields(self):
        """Test that filters are properly declared"""
        assert hasattr(UserFilterSet, '_declared_filters')
        assert "username" in UserFilterSet._declared_filters
        assert "email" in UserFilterSet._declared_filters
        assert "age" in UserFilterSet._declared_filters
        assert "is_active" in UserFilterSet._declared_filters
