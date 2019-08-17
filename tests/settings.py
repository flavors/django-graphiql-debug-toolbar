INSTALLED_APPS = [
    'graphiql_debug_toolbar',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

SECRET_KEY = 'test'
ROOT_URLCONF = 'tests.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'OPTIONS': {
        'loaders': [
            'django.template.loaders.app_directories.Loader',
        ],
    },
}]
