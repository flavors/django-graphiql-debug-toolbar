import functools
import json
from collections import OrderedDict

from django.template.loader import render_to_string
from django.utils.encoding import force_text

from debug_toolbar import middleware as mmod
from debug_toolbar.middleware import _HTML_TYPES
from debug_toolbar.middleware import DebugToolbarMiddleware as BaseMiddleware
from debug_toolbar.middleware import get_show_toolbar
from debug_toolbar.toolbar import DebugToolbar
from graphene_django.views import GraphQLView

from .serializers import CallableJSONEncoder

__all__ = ['DebugToolbarMiddleware']


class _DebugToolbar(DebugToolbar):
    def __init__(self, middleware, *args, **kwargs):
        middleware._toolbar = self
        super().__init__(*args, **kwargs)


class MockToolbar(object):
    def __init__(self, middleware):
        self._middleware = middleware

    def __enter__(self):
        mmod.DebugToolbar = functools.partial(_DebugToolbar, self._middleware)

    def __exit__(self, exc_type, exc_val, exc_tb):
        mmod.DebugToolbar = DebugToolbar


def set_content_length(response):
    if response.has_header('Content-Length'):
        response['Content-Length'] = str(len(response.content))


def get_payload(request, response, toolbar):
    content = force_text(response.content, encoding=response.charset)
    payload = json.loads(content, object_pairs_hook=OrderedDict)
    payload['debugToolbar'] = OrderedDict([('panels', OrderedDict())])

    for panel in reversed(toolbar.enabled_panels):
        if panel.panel_id == 'TemplatesPanel':
            continue

        panel.generate_stats(request, response)
        panel.generate_server_timing(request, response)

        if panel.has_content:
            title = panel.title
        else:
            title = None

        payload['debugToolbar']['panels'][panel.panel_id] = {
            'title': title,
            'subtitle': panel.nav_subtitle,
        }

    toolbar.store()
    payload['debugToolbar']['storeId'] = toolbar.store_id
    return payload


class DebugToolbarMiddleware(BaseMiddleware):

    def process_view(self, request, view_func, *args):
        if hasattr(view_func, 'view_class') and\
                issubclass(view_func.view_class, GraphQLView):
            request._graphql_view = True

    def __call__(self, request):
        if not get_show_toolbar()(request) or request.is_ajax():
            return self.get_response(request)

        with MockToolbar(self):
            response = super().__call__(request)
        content_type = response.get('Content-Type', '').split(';')[0]
        html_type = content_type in _HTML_TYPES
        graphql_view = getattr(request, '_graphql_view', False)

        if response.status_code == 200 and graphql_view and html_type:
            template = render_to_string('graphiql_debug_toolbar/base.html')
            response.write(template)
            set_content_length(response)

        if html_type or not (
                graphql_view and content_type == 'application/json'):
            return response

        toolbar = self._toolbar

        payload = get_payload(request, response, toolbar)
        response.content = json.dumps(payload, cls=CallableJSONEncoder)
        set_content_length(response)
        return response
