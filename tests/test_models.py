from flask_mongo_rest.mongo_models import MongoBaseModel


def test_insert_and_find(mock_collection):
    model = MongoBaseModel(mock_collection)

    result = model.insert_one({"name": "Alice"})
    doc = model.find_one({"_id": result.inserted_id})

    assert doc["name"] == "Alice"


def test_update(mock_collection):
    model = MongoBaseModel(mock_collection)
    result = model.insert_one({"name": "Bob"})

    model.update_one_by_id(result.inserted_id, {"name": "Updated"})
    doc = model.find_one({"_id": result.inserted_id})

    assert doc["name"] == "Updated"


def test_delete(mock_collection):
    model = MongoBaseModel(mock_collection)
    result = model.insert_one({"name": "Del"})

    model.delete_by_id(result.inserted_id)
    doc = model.find_one({"_id": result.inserted_id})

    assert doc is None