# serializers.py
from .models import ScanMonitorPathModel
from flask_mongo_drf import ModelSerializer, CharField, DateTimeField


class ScanMonitorPathSerializer(ModelSerializer):
    monitor_path = CharField(required=True, min_length=1)
    status = CharField(required=True, min_length=1, max_length=20)
    create_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        model = ScanMonitorPathModel
