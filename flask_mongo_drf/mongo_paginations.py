# mongo_pagination.py
import math
from flask import url_for


class MongoPagination:
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100

    def __init__(self, request_args, count, endpoint_name):
        self.request_args = request_args.to_dict() if hasattr(request_args, 'to_dict') else dict(request_args)
        self.count = count
        self.endpoint_name = endpoint_name  # 应为完整的端点名，如 'blueprint.list'
        self.page_number = 1
        self.current_page_size = self.page_size
        self._parse_pagination_params()

    def _parse_pagination_params(self):
        limit = self.request_args.get(self.page_size_query_param, str(self.page_size))
        try:
            self.current_page_size = max(1, min(int(limit), self.max_page_size))
        except (ValueError, TypeError):
            self.current_page_size = self.page_size
        page = self.request_args.get(self.page_query_param, '1')
        try:
            self.page_number = max(int(page), 1)
        except (ValueError, TypeError):
            self.page_number = 1

    @property
    def skip(self):
        return (self.page_number - 1) * self.current_page_size

    @property
    def limit(self):
        return self.current_page_size

    def get_next_link(self):
        if (self.page_number * self.current_page_size) >= self.count:
            return None
        args = self.request_args.copy()
        args[self.page_query_param] = str(self.page_number + 1)
        try:
            return url_for(self.endpoint_name, _external=True, **args)
        except Exception:
            return None

    def get_previous_link(self):
        if self.page_number <= 1:
            return None
        args = self.request_args.copy()
        args[self.page_query_param] = str(self.page_number - 1)
        try:
            return url_for(self.endpoint_name, _external=True, **args)
        except Exception:
            return None

    def get_meta(self) -> dict:
        total_pages = math.ceil(self.count / self.current_page_size) if self.current_page_size > 0 else 0
        return {
            'page_size': self.current_page_size,
            'current_page': self.page_number,
            'total_pages': total_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link()
        }
