from django.conf.urls import include, url

import debug_toolbar

urlpatterns = [
    url(r"^__debug__/", include(debug_toolbar.urls)),
]
