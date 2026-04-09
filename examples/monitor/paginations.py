from flask_mongo_rest import MongoPagination


class ScanMonitorPathPagination(MongoPagination):
    max_page_size = 200
