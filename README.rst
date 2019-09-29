Django GraphiQL Debug Toolbar
=============================

|Pypi| |Build Status| |Codecov|


Django `Debug Toolbar`_ for `GraphiQL`_ IDE

.. _GraphiQL: https://github.com/graphql/graphiql
.. _Debug Toolbar: https://github.com/jazzband/django-debug-toolbar


.. image:: https://user-images.githubusercontent.com/5514990/36340937-1937ee68-1419-11e8-8477-40622e98c312.gif

Dependencies
------------

* Python ≥ 3.4
* Django ≥ 1.11


Installation
------------

Install last stable version from Pypi.

.. code:: sh

    pip install django-graphiql-debug-toolbar


See the `documentation`_ for further guidance on setting *Django Debug Toolbar*.

.. _documentation: https://django-debug-toolbar.readthedocs.io/en/stable/installation.html

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

The *Debug Toolbar* is shown only if your IP is listed in the ``INTERNAL_IPS`` setting (you can change this logic with the ``SHOW_TOOLBAR_CALLBACK`` option).

.. code:: python

    INTERNAL_IPS = ['127.0.0.1', '...']

Dockerize ``INTERNAL_IPS``

.. code:: python

    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1' for ip in ips]


Limitations
-----------

Panels rendering is not supported in multiprocess environment.

----

Credits to `@jazzband`_ / `django-debug-toolbar`_.

.. _@jazzband: https://jazzband.co
.. _django-debug-toolbar: https://github.com/jazzband/django-debug-toolbar


.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphiql-debug-toolbar.svg
   :target: https://pypi.python.org/pypi/django-graphiql-debug-toolbar

.. |Build Status| image:: https://travis-ci.org/flavors/django-graphiql-debug-toolbar.svg?branch=master
   :target: https://travis-ci.org/flavors/django-graphiql-debug-toolbar

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/django-graphiql-debug-toolbar.svg
   :target: https://codecov.io/gh/flavors/django-graphiql-debug-toolbar
