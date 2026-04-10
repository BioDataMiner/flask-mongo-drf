Models
======

`MongoBaseModel` is the base model class that wraps common PyMongo Collection operations.

Usage
-----

Inherit `MongoBaseModel` and inject a `Collection` instance in `__init__`:

.. code-block:: python

   from flask_mongo_drf import MongoBaseModel
   from flask_mongo_drf.contrib import MongoDBManager

   class UserModel(MongoBaseModel):
       def __init__(self):
           collection = MongoDBManager.get_collection("users", client_name="default")
           super().__init__(collection)

Available Methods
-----------------

- `count_documents(query)` — count documents
- `find_all(query, sort_by, sort_order)` — returns cursor
- `find_paginated(query, skip, limit, sort_by, sort_order)` — paginated query
- `insert_one(data)` — inserts, auto adds `create_time` and `update_time`
- `update_one_by_id(doc_id, data)` — partial update (PATCH)
- `replace_by_id(doc_id, new_doc)` — full replace (PUT)
- `delete_by_id(doc_id)` — delete
- `find_one(query)` — single document
- `aggregate(pipeline)` — aggregation pipeline