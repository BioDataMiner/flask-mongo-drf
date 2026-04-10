Testing
=======

The framework uses `pytest` + `mongomock` for testing.

Run Tests
---------

.. code-block:: bash

   pytest tests/ --cov=flask_mongo_drf

Example Test
------------

.. code-block:: python

   import pytest
   from mongomock import MongoClient
   from flask_mongo_drf import MongoBaseModel

   def test_insert():
       client = MongoClient()
       collection = client.test.users
       model = MongoBaseModel(collection)
       result = model.insert_one({"name": "Alice"})
       assert result.inserted_id is not None