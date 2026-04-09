from flask import Blueprint
from .views import ScanMonitorPathViewSet

monitor_bp = Blueprint('monitor', __name__)

# 5. Register the routes with the Flask Blueprint
ScanMonitorPathViewSet.register_routes(monitor_bp, "monitor-paths", actions=["list", "create", "update", "retrieve"])