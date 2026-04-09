# flask_mongo_rest/contrib/mongodb_manager.py
import logging
from typing import Dict, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ConfigurationError

from flask_mongo_rest import MongoDBConnectionError

logger = logging.getLogger(__name__)


class MongoDBManager:
    """
    解耦版 MongoDB 数据库管理器：
    - 管理底层 MongoClient 的连接与释放
    - 提供静态方法，方便业务层获取 Collection 实例
    - 支持连接池配置、默认数据库缓存、Flask 应用工厂集成
    """
    _clients: Dict[str, MongoClient] = {}
    _default_dbs: Dict[str, Optional[str]] = {}

    @classmethod
    def register_client(
            cls,
            name: str,
            uri: str,
            default_db: str = None,
            **kwargs
    ) -> MongoClient:
        """
        注册并初始化 MongoDB 客户端。

        :param name: 客户端唯一标识
        :param uri: MongoDB 连接 URI
        :param default_db: 默认数据库名（可选，用于 get_collection 简化调用）
        :param kwargs: 额外参数（如 maxPoolSize, minPoolSize 等）
        :return: MongoClient 实例
        :raises MongoDBConnectionError: 连接失败时抛出
        """
        if name in cls._clients:
            cls._clients[name].close()

        # 默认连接池配置
        default_kwargs = {
            "maxPoolSize": 50,
            "minPoolSize": 10,
            "serverSelectionTimeoutMS": 5000,
            "retryWrites": True,
        }
        default_kwargs.update(kwargs)
        try:
            client = MongoClient(uri, **default_kwargs)
            # 测试连接
            client.admin.command('ping')
            cls._clients[name] = client
            if default_db:
                cls._default_dbs[name] = default_db
            logger.info(f"MongoDB client '{name}' registered (default DB: {default_db})")
            return client
        except (ConnectionFailure, ConfigurationError) as e:
            logger.error(f"Failed to connect to MongoDB '{name}': {e}")
            raise MongoDBConnectionError(f"Could not connect to MongoDB '{name}'") from e

    @classmethod
    def get_client(cls, name: str = "default") -> MongoClient:
        """获取已注册的客户端"""
        if name not in cls._clients:
            raise RuntimeError(f"MongoDB client '{name}' not registered. Call register_client first.")
        return cls._clients[name]

    @classmethod
    def get_database(cls, db_name: str = None, client_name: str = "default"):
        """
        获取数据库实例。

        :param db_name: 数据库名，若为 None 则使用注册时的默认数据库
        :param client_name: 客户端名称
        :return: 数据库实例
        """
        client = cls.get_client(client_name)
        target_db = db_name or cls._default_dbs.get(client_name)
        if not target_db:
            raise ValueError(f"No database name provided for client '{client_name}'")
        return client[target_db]

    @classmethod
    def get_collection(
            cls,
            collection_name: str,
            db_name: str = None,
            client_name: str = "default"
    ) -> Collection:
        """
        获取 Collection 实例（最常用）。

        :param collection_name: 集合名称
        :param db_name: 数据库名（可选，默认使用客户端注册时的默认数据库）
        :param client_name: 客户端名称
        :return: Collection 实例
        """
        db = cls.get_database(db_name, client_name)
        return db[collection_name]

    @classmethod
    def close_all(cls):
        """关闭所有已注册的 MongoDB 连接"""
        for client in cls._clients.values():
            client.close()
        cls._clients.clear()
        cls._default_dbs.clear()

    @property
    def clients(self):
        return self._clients


def init_mongodb(app):
    """
    从 Flask 应用配置中批量初始化 MongoDB 连接。

    配置格式：
        app.config["MONGODB_SETTINGS"] = {
            "default": {"host": "mongodb://localhost:27017", "db": "myapp"},
            "analytics": {"host": "mongodb://...", "db": "logs", "maxPoolSize": 20}
        }

    注意：不再自动从环境变量 MONGO_URI/MONGO_DB 降级，请显式配置。
    """
    mongo_configs = app.config.get("MONGODB_SETTINGS")
    if not mongo_configs:
        logger.warning(
            "No MONGODB_SETTINGS found in app.config. "
            "Please define MONGODB_SETTINGS to use MongoDBManager."
        )
        return

    for name, config in mongo_configs.items():
        uri = config.get("host")
        db = config.get("db")
        if not uri or not db:
            logger.error(f"Invalid MongoDB config for '{name}': missing 'host' or 'db'")
            continue
        # 提取额外参数（除 host, db 外的键值对）
        extra = {k: v for k, v in config.items() if k not in ("host", "db")}
        MongoDBManager.register_client(name, uri, default_db=db, **extra)
