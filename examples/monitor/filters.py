from flask_mongo_drf import FilterSet, CharFilter


class ScanMonitorPathFilter(FilterSet):
    monitor_path = CharFilter(lookup_expr='icontains', help_text='扫描路径')
    status = CharFilter(lookup_expr='icontains', help_text='扫描路径状态')

    class Meta:
        pass
