Routing
=======

The `register_routes` method automatically generates standard REST routes for a ViewSet.

Parameters
----------

- `blueprint` — Flask Blueprint instance
- `url_prefix` — URL prefix
- `actions` — optional, list of actions to register (default all)

Example
-------

.. code-block:: python

   # Register only list and create
   UserViewSet.register_routes(bp, 'users', actions=['list', 'create'])