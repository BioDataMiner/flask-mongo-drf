Aggregation
===========

Override `get_pipeline` in ViewSet to use MongoDB aggregation pipelines.

Example
-------

.. code-block:: python

   class SalesViewSet(MongoModelViewSet):
       def get_pipeline(self, filter_dict):
           return [
               {"$match": filter_dict},
               {"$group": {"_id": "$product", "total_sales": {"$sum": "$amount"}}},
               {"$sort": {"total_sales": -1}}
           ]

The framework handles pagination and counting automatically.