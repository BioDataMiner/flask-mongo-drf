Error Handling
==============

The framework provides unified exception handling and response format.

Exception Classes
-----------------

- `APIException` — base class
- `ValidationError` (400)
- `AuthenticationFailed` (401)
- `PermissionDenied` (403)
- `NotFound` (404)

Response Format
---------------

All exception responses follow:

.. code-block:: json

   {
     "code": 400,
     "message": "Validation failed",
     "results": null,
     "total": 0,
     "success": false
   }

Custom Exception
----------------

Inherit `APIException` and set `code` and `message`.