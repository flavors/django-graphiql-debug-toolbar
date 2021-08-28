# Django GraphiQL Debug Toolbar

[![Tests](https://github.com/flavors/django-graphiql-debug-toolbar/actions/workflows/test-suite.yml/badge.svg)](https://github.com/flavors/django-graphiql-debug-toolbar/actions)
[![Coverage](https://img.shields.io/codecov/c/github/flavors/django-graphiql-debug-toolbar?color=%2334D058)](https://codecov.io/gh/flavors/django-graphiql-debug-toolbar)
[![Codacy](https://app.codacy.com/project/badge/Grade/354f70cdefda40938c397d8651a2a06c)](https://www.codacy.com/gh/flavors/django-graphiql-debug-toolbar/dashboard)
[![Package version](https://img.shields.io/pypi/v/django-graphiql-debug-toolbar.svg)](https://pypi.python.org/pypi/django-graphiql-debug-toolbar)

[Django Debug Toolbar](https://github.com/jazzband/django-debug-toolbar) for [GraphiQL](https://github.com/graphql/graphiql) IDE.

![Graphiql Debug Toolbar](https://user-images.githubusercontent.com/5514990/36340937-1937ee68-1419-11e8-8477-40622e98c312.gif)

## Dependencies

*   Python ≥ 3.6
*   Django ≥ 2.2

## Installation

Install last stable version from Pypi.

```sh
pip install django-graphiql-debug-toolbar
````

See the [documentation](https://django-debug-toolbar.readthedocs.io/en/stable/installation.html) for further guidance on setting *Django Debug Toolbar*.

Add `graphiql_debug_toolbar` to your *INSTALLED_APPS* settings:

```py
INSTALLED_APPS = [
    'debug_toolbar',
    'graphiql_debug_toolbar',
]
```

**Replace** the Django Debug Toolbar **middleware** with the GraphiQL Debug Toolbar one. 

```py
MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'graphiql_debug_toolbar.middleware.DebugToolbarMiddleware',
]
```

Credits to [@jazzband](https://jazzband.co) / [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar).
