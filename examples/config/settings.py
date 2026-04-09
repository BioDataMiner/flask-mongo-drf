# config/setting.py
import os
from urllib.parse import quote_plus


def get_mongo_uri(
        user_env: str,
        pass_env: str,
        host_env: str,
        port_env: str,
        db_env: str = None,
        fallback_db: str = None,
        **extra_options
) -> str:
    """
    从环境变量构造 MongoDB URI，并支持额外参数拼接。

    :param user_env: 用户名的环境变量名
    :param pass_env: 密码的环境变量名
    :param host_env: 主机名的环境变量名
    :param port_env: 端口的环境变量名
    :param db_env: 数据库名的环境变量名（可选）
    :param fallback_db: 当 db_env 未设置时的默认数据库名
    :param extra_options: 额外连接参数，如 maxPoolSize=50
    :return: MongoDB URI 字符串
    :raises ValueError: 缺少必要环境变量时抛出
    """
    username = os.getenv(user_env)
    password = os.getenv(pass_env)
    if not username or not password:
        raise ValueError(f"Missing MongoDB credentials: {user_env} or {pass_env}")

    username = quote_plus(username)
    password = quote_plus(password)

    host = os.getenv(host_env, "localhost")
    port = os.getenv(port_env, "27017")

    db_name = None
    if db_env:
        db_name = os.getenv(db_env)
    if not db_name:
        db_name = fallback_db
    if not db_name:
        raise ValueError(f"Database name not provided for {db_env or 'fallback_db'}")
    uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource=admin"
    if extra_options:
        uri += "&" + "&".join(f"{k}={v}" for k, v in extra_options.items())
    return uri


class Config:
    DEBUG = os.getenv('DEBUG', '').lower() in ('true', '1', 't')

    MONGODB_SETTINGS = {
        "blood": {
            "host": get_mongo_uri(
                "MONGO_USER", "MONGO_PASS", "MONGO_HOST", "MONGO_PORT",
                db_env="BLOOD_DB_NAME", fallback_db="Blood",
                maxPoolSize=50
            ),
            "db": "Blood",
        },
        "tumor": {
            "host": get_mongo_uri(
                "MONGO_USER", "MONGO_PASS", "MONGO_HOST", "MONGO_PORT",
                db_env="TUMOR_DB_NAME", fallback_db="Tumor",
                maxPoolSize=100
            ),
            "db": "Tumor",
        },
    }
