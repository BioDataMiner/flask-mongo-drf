# mongo_filters.py
import re
import logging

from bson import ObjectId
from typing import Any, Dict
from datetime import datetime
from collections import OrderedDict

from .mongo_exceptions import ValidationError

logger = logging.getLogger(__name__)


class Filter:
    def __init__(self, field_name: str = None, lookup_expr: str = 'exact', method: str = None, help_text: str = None):
        self.field_name = field_name
        self.lookup_expr = lookup_expr
        self.method = method
        self.help_text = help_text
        self.parent = None

    def filter(self, value: Any) -> Dict[str, Any]:
        if value is None or value == '':
            return {}
        if self.method and self.parent:
            method_func = getattr(self.parent, self.method, None)
            if callable(method_func):
                return method_func(value)
        expr = self._get_mongo_expression(value)
        return {self.field_name: expr}

    def _get_mongo_expression(self, value: Any) -> Any:
        lookup_map = {
            'exact': value,
            'iexact': {"$regex": f"^{re.escape(str(value))}$", "$options": "i"},
            'contains': {"$regex": re.escape(str(value))},
            'icontains': {"$regex": re.escape(str(value)), "$options": "i"},
            'gt': {"$gt": value},
            'gte': {"$gte": value},
            'lt': {"$lt": value},
            'lte': {"$lte": value},
            'ne': {"$ne": value},
            'in': {"$in": value if isinstance(value, list) else str(value).split(',')},
            'exists': {"$exists": str(value).lower() in ('true', '1', 'yes')},
        }
        return lookup_map.get(self.lookup_expr, value)


class CharFilter(Filter):
    pass


class NumberFilter(Filter):
    def filter(self, value: Any) -> Dict[str, Any]:
        if value is None or value == '':
            return {}
        try:
            if "." in str(value):
                value = float(value)
            else:
                value = int(value)
        except (ValueError, TypeError):
            logger.debug(f"Ignoring invalid number value for {self.field_name}: {value}")
            return {}
        return super().filter(value)


class BooleanFilter(Filter):
    def filter(self, value: Any) -> Dict[str, Any]:
        if value is None or value == '':
            return {}
        bool_val = str(value).lower() in ('true', '1', 'yes', 't', 'y')
        return super().filter(bool_val)


class DateFilter(Filter):
    def __init__(self, field_name: str = None, lookup_expr: str = 'exact', date_format: str = '%Y-%m-%d', **kwargs):
        super().__init__(field_name, lookup_expr, **kwargs)
        self.date_format = date_format

    def filter(self, value: Any) -> Dict[str, Any]:
        if not value:
            return {}
        try:
            dt_value = datetime.strptime(str(value), self.date_format) if isinstance(value, str) else value
            return super().filter(dt_value)
        except:
            raise ValidationError(f"Invalid date format for {self.field_name}, expected {self.date_format}")


class ObjectIdFilter(Filter):
    def filter(self, value: Any) -> Dict[str, Any]:
        if not value:
            return {}
        try:
            if self.lookup_expr == 'in':
                vals = value if isinstance(value, list) else str(value).split(',')
                oids = [ObjectId(v.strip()) for v in vals if ObjectId.is_valid(v.strip())]
                if not oids:
                    return {}
                value = oids
            else:
                if not ObjectId.is_valid(str(value)):
                    return {}
                value = ObjectId(str(value))
            return super().filter(value)
        except:
            return {}


class FilterSetMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        declared_filters = OrderedDict()
        for base in bases:
            if hasattr(base, '_declared_filters'):
                declared_filters.update(base._declared_filters)
        current_filters = []
        for key, value in attrs.items():
            if isinstance(value, Filter):
                if not value.field_name:
                    value.field_name = key
                current_filters.append((key, value))
        for key, value in current_filters:
            declared_filters[key] = value
        meta = attrs.get('Meta')
        if meta and hasattr(meta, 'fields'):
            fields = meta.fields
            if isinstance(fields, dict):
                for field_name, lookups in fields.items():
                    for lookup in lookups:
                        filter_name = f"{field_name}__{lookup}" if lookup != 'exact' else field_name
                        declared_filters[filter_name] = Filter(field_name=field_name, lookup_expr=lookup)
            elif isinstance(fields, list):
                for field_name in fields:
                    declared_filters[field_name] = Filter(field_name=field_name, lookup_expr='exact')
        attrs['_declared_filters'] = declared_filters
        return super().__new__(mcs, name, bases, attrs)


class FilterSet(metaclass=FilterSetMetaclass):
    def __init__(self, data: Dict[str, Any] = None, request=None):
        self.data = data or {}
        self.request = request
        for filter_obj in self._declared_filters.values():
            filter_obj.parent = self

    def get_query_dict(self) -> Dict[str, Any]:
        query_dict = {}
        for name, filter_obj in self._declared_filters.items():
            value = self.data.get(name)
            if value is not None and value != '':
                filter_result = filter_obj.filter(value)
                if not filter_result:
                    continue
                for field, expr in filter_result.items():
                    if field not in query_dict:
                        query_dict[field] = expr
                    else:
                        if isinstance(query_dict[field], dict) and isinstance(expr, dict):
                            query_dict[field].update(expr)
                        else:
                            query_dict[field] = expr
        return query_dict
