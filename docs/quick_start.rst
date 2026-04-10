Quick Start
===========

1. Create Flask app and configure MongoDB
------------------------------------------

.. code-block:: python

   from flask import Flask
   from pymongo import MongoClient
   from flask_mongo_drf import MongoModelViewSet, ModelSerializer, CharField
   from flask_mongo_drf.contrib import MongoDBManager

   app = Flask(__name__)

   # Register MongoDB client
   MongoDBManager.register_client("default", "mongodb://localhost:27017", default_db="testdb")

2. Define model and serializer
------------------------------

.. code-block:: python

   from flask_mongo_drf import MongoBaseModel

   class UserModel(MongoBaseModel):
       def __init__(self):
           collection = MongoDBManager.get_collection("users", client_name="default")
           super().__init__(collection)

   class UserSerializer(ModelSerializer):
       name = CharField(required=True, max_length=50)
       email = CharField(required=True)

       class Meta:
           model = UserModel

3. Write ViewSet and register routes
------------------------------------

.. code-block:: python

   from flask_mongo_drf import MongoModelViewSet
   from flask import Blueprint

   class UserViewSet(MongoModelViewSet):
       model_class = UserModel
       serializer_class = UserSerializer

   bp = Blueprint('api', __name__)
   UserViewSet.register_routes(bp, 'users')
   app.register_blueprint(bp, url_prefix='/api/v1')

4. Run the app
--------------

.. code-block:: bash

   flask run

Now you can access the following endpoints:

- `GET /api/v1/users/` — list
- `POST /api/v1/users/` — create
- `GET /api/v1/users/<id>` — retrieve
- `PUT /api/v1/users/<id>` — full update
- `PATCH /api/v1/users/<id>` — partial update
- `DELETE /api/v1/users/<id>` — delete

Swagger documentation is automatically available at `/apidocs/`.