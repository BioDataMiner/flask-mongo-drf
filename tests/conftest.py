import pytest
from flask import Flask
from bson import ObjectId


class MockCollection:
    def __init__(self):
        self.data = []

    def insert_one(self, doc):
        doc["_id"] = ObjectId()
        self.data.append(doc)
        return type("obj", (), {"inserted_id": doc["_id"]})

    def find_one(self, query):
        for d in self.data:
            if d["_id"] == query["_id"]:
                return d
        return None

    def count_documents(self, query):
        return len(self.data)

    def find(self, query):
        return iter(self.data)

    def update_one(self, query, update):
        for d in self.data:
            if d["_id"] == query["_id"]:
                d.update(update["$set"])
                return type("obj", (), {"matched_count": 1, "modified_count": 1})
        return type("obj", (), {"matched_count": 0, "modified_count": 0})

    def replace_one(self, query, new_doc):
        for i, d in enumerate(self.data):
            if d["_id"] == query["_id"]:
                self.data[i] = new_doc
                return type("obj", (), {"matched_count": 1, "modified_count": 1})
        return type("obj", (), {"matched_count": 0, "modified_count": 0})

    def delete_one(self, query):
        for d in self.data:
            if d["_id"] == query["_id"]:
                self.data.remove(d)
                return type("obj", (), {"deleted_count": 1})
        return type("obj", (), {"deleted_count": 0})


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_collection():
    return MockCollection()