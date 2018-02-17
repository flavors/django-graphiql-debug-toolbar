Django GraphiQL Debug Toolbar
=============================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|


Django `Debug Toolbar`_ for `GraphiQL`_ IDE

.. _GraphiQL: https://github.com/graphql/graphiql
.. _Debug Toolbar: https://github.com/jazzband/django-debug-toolbar


.. image:: https://user-images.githubusercontent.com/5514990/36340937-1937ee68-1419-11e8-8477-40622e98c312.gif
   :width: 835
   :height: 398

Dependencies
------------

* Python ≥ 3.4
* Django ≥ 1.11


Installation
------------

Install last stable version from Pypi.

.. code:: sh

    pip install django-graphiql-debug-toolbar


Add ``graphiql_debug_toolbar`` to your *INSTALLED_APPS* settings:

.. code:: python

    INSTALLED_APPS = [
        ...
        'debug_toolbar',
        'graphiql_debug_toolbar',
    ]


**Replace** the Django Debug Toolbar **middleware** with the GraphiQL Debug Toolbar one. 

.. code:: python

    MIDDLEWARE = [
        ...
        # 'debug_toolbar.middleware.DebugToolbarMiddleware',
        'graphiql_debug_toolbar.middleware.DebugToolbarMiddleware',
        ...
    ]

----

Credits to `@jazzband`_ / `django-debug-toolbar`_.

.. _@jazzband: https://jazzband.co
.. _django-debug-toolbar: https://github.com/jazzband/django-debug-toolbar


.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphiql-debug-toolbar.svg
   :target: https://pypi.python.org/pypi/django-graphiql-debug-toolbar

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-graphiql-debug-toolbar.svg
   :target: https://pypi.python.org/pypi/django-graphiql-debug-toolbar

.. |Build Status| image:: https://travis-ci.org/flavors/django-graphiql-debug-toolbar.svg?branch=master
   :target: https://travis-ci.org/flavors/django-graphiql-debug-toolbar

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/django-graphiql-debug-toolbar.svg
   :target: https://codecov.io/gh/flavors/django-graphiql-debug-toolbar

.. |Code Climate| image:: https://api.codeclimate.com/v1/badges/.../maintainability
   :target: https://codeclimate.com/github/flavors/django-graphiql-debug-toolbar
