from flask_mongo_drf import MongoBaseModel
from flask_mongo_drf.contrib import MongoDBManager


class ScanMonitorPathModel(MongoBaseModel):
    """
    业务模型：
    在实例化时，通过 MongoDBManager.get_collection() 获取 Collection 并注入基类。
    """

    def __init__(self):
        # 1. 获取特定客户端和数据库中的集合
        collection = MongoDBManager.get_collection(
            collection_name="scan_monitor_path",
            client_name="tumor"
        )
        # 2. 注入到基类中
        super().__init__(collection=collection)
