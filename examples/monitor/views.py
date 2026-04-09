from flask_mongo_drf import MongoModelViewSet

from .models import ScanMonitorPathModel
from .filters import ScanMonitorPathFilter
from .serializers import ScanMonitorPathSerializer
from .paginations import ScanMonitorPathPagination


class ScanMonitorPathViewSet(MongoModelViewSet):
    model_class = ScanMonitorPathModel
    filterset_class = ScanMonitorPathFilter
    serializer_class = ScanMonitorPathSerializer
    pagination_class = ScanMonitorPathPagination
    default_sort_by = "uploadTime"
    default_sort_order = -1  # Descending
