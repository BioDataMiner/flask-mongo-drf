import pytest
from flask import Flask, Blueprint
from unittest.mock import MagicMock, patch
from bson.objectid import ObjectId

# 直接导入你的类
from flask_mongo_drf import MongoModelViewSet
from flask_mongo_drf import Serializer, CharField


# ------------------------------
# 测试用的序列化器
# ------------------------------
class UserSerializer(Serializer):
    name = CharField(required=True)


# ------------------------------
# 测试用 ViewSet（完全符合你的框架要求）
# ------------------------------
class UserViewSet(MongoModelViewSet):
    serializer_class = UserSerializer
    collection = None  # 必须这么写，不能写 __init__


# ------------------------------
# 路由注册
# ------------------------------
def register(app, collection):
    bp = Blueprint("test", __name__)

    # 注册前赋值 collection
    UserViewSet.collection = collection

    # 注册路由
    UserViewSet.register_routes(bp, "users")
    app.register_blueprint(bp)


# ------------------------------
# Fixtures
# ------------------------------
@pytest.fixture(autouse=True)
def clean_state():
    """每个测试自动清空，避免交叉污染"""
    UserViewSet.collection = None
    yield


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_collection():
    """构造完整可用的 mock collection"""
    coll = MagicMock()

    # 模拟 insert_one
    mock_id = ObjectId()
    coll.insert_one.return_value.inserted_id = mock_id

    # 模拟 find_one
    coll.find_one.return_value = {
        "_id": mock_id,
        "name": "test"
    }

    # 模拟 count
    coll.count_documents.return_value = 1

    # 模拟 find_all
    mock_cursor = MagicMock()
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.__iter__.return_value = iter([{
        "_id": mock_id,
        "name": "test"
    }])
    coll.find_all.return_value = mock_cursor

    # 模拟删除
    coll.delete_by_id.return_value.deleted_count = 1

    return coll


# ------------------------------
# 测试用例
# ------------------------------
def test_create_user(client, app, mock_collection):
    register(app, mock_collection)
    resp = client.post("/users", json={"name": "Alice"})
    assert resp.status_code == 201
    assert "id" in resp.json


def test_list_users(client, app, mock_collection):
    register(app, mock_collection)
    resp = client.get("/users")
    assert resp.status_code == 200
    assert resp.json["total"] == 1


def test_retrieve_user(client, app, mock_collection):
    register(app, mock_collection)
    resp = client.post("/users", json={"name": "Bob"})
    doc_id = resp.json["id"]

    resp = client.get(f"/users/{doc_id}")
    assert resp.status_code == 200
    assert "data" in resp.json


def test_delete_user(client, app, mock_collection):
    register(app, mock_collection)
    resp = client.post("/users", json={"name": "Charlie"})
    doc_id = resp.json["id"]

    resp = client.delete(f"/users/{doc_id}")
    assert resp.status_code == 204