Serializers
===========

Serializers handle:
- Input data validation and conversion (deserialization)
- Output data formatting (serialization)

Define a Serializer
-------------------

Inherit `ModelSerializer` and declare fields:

.. code-block:: python

   from flask_mongo_drf import ModelSerializer, CharField, IntegerField

   class UserSerializer(ModelSerializer):
       name = CharField(required=True, max_length=50)
       age = IntegerField(min_value=0, max_value=150)

       class Meta:
           model = UserModel   # optional

Built-in Field Types
--------------------

- `CharField` — string, supports `max_length`, `min_length`
- `IntegerField` — integer, supports `min_value`, `max_value`
- `FloatField` — float
- `BooleanField` — boolean
- `DateTimeField` — datetime, custom format
- `ObjectIdField` — MongoDB ObjectId
- `ListField` — list, can nest child fields
- `DictField` — dictionary

Field Options
-------------

- `required` — whether required
- `default` — default value
- `allow_null` — allow null
- `read_only` — output only, not for input
- `write_only` — input only, not for output
- `validators` — list of custom validation functions

Using Serializers
-----------------

Automatically used in ViewSet, or manually:

.. code-block:: python

   serializer = UserSerializer(data=request.json)
   if serializer.is_valid():
       validated_data = serializer.validated_data
   else:
       errors = serializer.errors