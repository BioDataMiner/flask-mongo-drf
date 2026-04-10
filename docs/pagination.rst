Pagination
==========

The framework provides `MongoPagination` with `page` and `page_size` parameters.

Custom Pagination
-----------------

Inherit `MongoPagination` and override class attributes:

.. code-block:: python

   from flask_mongo_drf import MongoPagination

   class CustomPagination(MongoPagination):
       page_size = 20
       max_page_size = 200

Use in ViewSet
--------------

.. code-block:: python

   class UserViewSet(MongoModelViewSet):
       pagination_class = CustomPagination

Request Example
---------------

`GET /users/?page=2&page_size=10`

Response includes pagination metadata:

.. code-block:: json

   {
     "total": 100,
     "current_page": 2,
     "total_pages": 10,
     "page_size": 10,
     "next": "http://.../?page=3&page_size=10",
     "previous": "http://.../?page=1&page_size=10",
     "results": [...]
   }