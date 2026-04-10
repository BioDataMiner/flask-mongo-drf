Multi-Database Support
======================

`MongoDBManager` can manage multiple MongoDB connections.

Configuration Example
---------------------

Define `MONGODB_SETTINGS` in Flask config:

.. code-block:: python

   app.config["MONGODB_SETTINGS"] = {
       "default": {"host": "mongodb://localhost:27017", "db": "main"},
       "analytics": {"host": "mongodb://analytics:27017", "db": "logs"}
   }

   from flask_mongo_drf.contrib import init_mongodb
   init_mongodb(app)

Use in Model
------------

.. code-block:: python

   class LogModel(MongoBaseModel):
       def __init__(self):
           collection = MongoDBManager.get_collection("logs", client_name="analytics")
           super().__init__(collection)