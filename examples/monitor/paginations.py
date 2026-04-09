from flask_mongo_drf import MongoPagination


class ScanMonitorPathPagination(MongoPagination):
    max_page_size = 200
