Custom Serializers
==================

You can create custom fields or override validation logic.

Custom Field
------------

Inherit `Field` and implement `to_representation` and `to_internal_value`:

.. code-block:: python

   from flask_mongo_drf import Field, ValidationError

   class PhoneField(Field):
       def to_internal_value(self, value):
           if not value.startswith('+'):
               raise ValidationError("Phone number must start with '+'")
           return value

Use in Serializer
-----------------

.. code-block:: python

   class UserSerializer(ModelSerializer):
       phone = PhoneField(required=True)