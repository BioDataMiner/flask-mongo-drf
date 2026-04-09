import pytest
from unittest.mock import MagicMock, patch

from flask_mongo_rest.contrib.mongodb_manager import MongoDBManager


# -----------------------------
# 通用 fixture：mock MongoClient
# -----------------------------
@pytest.fixture(autouse=True)
def clean_mongo_manager():
    """ 每个测试自动执行：清空 MongoDBManager 类变量，防止测试污染 """
    MongoDBManager._clients = {}
    MongoDBManager._default_dbs = {}
    yield
    MongoDBManager._clients = {}
    MongoDBManager._default_dbs = {}


@pytest.fixture
def mock_mongo_client():
    with patch("flask_mongo_rest.contrib.mongodb_manager.MongoClient") as MockClient:
        mock_client_instance = MagicMock()
        mock_client_instance.admin.command.return_value = {"ok": 1}

        mock_db = MagicMock()
        mock_collection = MagicMock()

        mock_client_instance.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        MockClient.return_value = mock_client_instance

        yield MockClient, mock_client_instance, mock_db, mock_collection


# -----------------------------
# test register_client + get_client
# -----------------------------
def test_register_and_get_client(mock_mongo_client):
    MockClient, mock_client, _, _ = mock_mongo_client

    client = MongoDBManager.register_client(
        name="test",
        uri="mongodb://fake:27017",
        default_db="test_db"
    )

    assert client == mock_client
    assert MongoDBManager.get_client("test") == mock_client

    # 验证 ping 被调用
    mock_client.admin.command.assert_called_with("ping")


# -----------------------------
# test get_database
# -----------------------------
def test_get_database(mock_mongo_client):
    _, mock_client, mock_db, _ = mock_mongo_client

    MongoDBManager.register_client(
        name="test",
        uri="mongodb://fake:27017",
        default_db="test_db"
    )

    db = MongoDBManager.get_database(client_name="test")

    assert db == mock_db
    mock_client.__getitem__.assert_called_with("test_db")


# -----------------------------
# test get_collection
# -----------------------------
def test_get_collection(mock_mongo_client):
    _, _, mock_db, mock_collection = mock_mongo_client

    MongoDBManager.register_client(
        name="test",
        uri="mongodb://fake:27017",
        default_db="test_db"
    )

    collection = MongoDBManager.get_collection(
        "my_collection",
        client_name="test"
    )

    assert collection == mock_collection
    mock_db.__getitem__.assert_called_with("my_collection")


# -----------------------------
# test missing client
# -----------------------------
def test_get_client_not_registered():
    with pytest.raises(RuntimeError):
        MongoDBManager.get_client("not_exist")


# -----------------------------
# test missing db name
# -----------------------------
def test_get_database_no_default(mock_mongo_client):
    MongoDBManager.register_client(
        name="test",
        uri="mongodb://fake:27017",
        default_db=None
    )

    # 加调试
    print(MongoDBManager._default_dbs)  # 看这里是不是空

    with pytest.raises(ValueError):
        MongoDBManager.get_database(client_name="test")


# -----------------------------
# test close_all
# -----------------------------
def test_close_all(mock_mongo_client):
    _, mock_client, _, _ = mock_mongo_client

    MongoDBManager.register_client(
        name="test",
        uri="mongodb://fake:27017",
        default_db="test_db"
    )

    MongoDBManager.close_all()

    mock_client.close.assert_called()
    assert MongoDBManager._clients == {}
    assert MongoDBManager._default_dbs == {}


# -----------------------------
# test init_mongodb
# -----------------------------
def test_init_mongodb(mock_mongo_client):
    from flask import Flask
    from flask_mongo_rest.contrib.mongodb_manager import init_mongodb

    app = Flask(__name__)
    app.config["MONGODB_SETTINGS"] = {
        "default": {
            "host": "mongodb://fake:27017",
            "db": "test_db",
            "maxPoolSize": 20
        }
    }

    init_mongodb(app)

    client = MongoDBManager.get_client("default")
    assert client is not None
