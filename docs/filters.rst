Filters
=======

Filters convert query parameters into MongoDB query conditions automatically.

Define a FilterSet
------------------

Inherit `FilterSet` and declare fields:

.. code-block:: python

   from flask_mongo_drf import FilterSet, CharFilter, NumberFilter

   class UserFilter(FilterSet):
       name = CharFilter(lookup_expr='icontains')   # case-insensitive contains
       age = NumberFilter(lookup_expr='gte')        # greater than or equal

Usage in ViewSet
----------------

Set `filterset_class` in ViewSet:

.. code-block:: python

   class UserViewSet(MongoModelViewSet):
       model_class = UserModel
       filterset_class = UserFilter

Then clients can send:
`GET /users/?name=john&age__gte=18`

Built-in Filter Types
---------------------

- `CharFilter` — string fields
- `NumberFilter` — numeric fields
- `BooleanFilter` — boolean fields
- `DateFilter` — date fields
- `ObjectIdFilter` — ObjectId fields

Supported Lookup Expressions
----------------------------

`exact`, `iexact`, `contains`, `icontains`, `gt`, `gte`, `lt`, `lte`, `ne`, `in`, `exists`