ViewSets
========

`MongoModelViewSet` provides standard CRUD operations.

Basic Usage
-----------

.. code-block:: python

   from flask_mongo_drf import MongoModelViewSet

   class UserViewSet(MongoModelViewSet):
       model_class = UserModel
       serializer_class = UserSerializer
       filterset_class = UserFilter
       pagination_class = CustomPagination
       default_sort_by = "created_at"
       default_sort_order = -1   # descending

Available Actions
-----------------

- `list` — GET /
- `create` — POST /
- `retrieve` — GET /<id>
- `update` — PUT /<id>
- `partial_update` — PATCH /<id>
- `destroy` — DELETE /<id>

Custom Aggregation
------------------

Override `get_pipeline` to use aggregation pipelines:

.. code-block:: python

   class ReportViewSet(MongoModelViewSet):
       def get_pipeline(self, filter_dict):
           return [
               {"$match": filter_dict},
               {"$group": {"_id": "$category", "total": {"$sum": 1}}}
           ]

Route Registration
------------------

.. code-block:: python

   from flask import Blueprint
   bp = Blueprint('api', __name__)
   UserViewSet.register_routes(bp, 'users')
   app.register_blueprint(bp, url_prefix='/api/v1')