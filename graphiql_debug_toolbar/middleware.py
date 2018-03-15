import json
import threading
from collections import OrderedDict

from django.template.loader import render_to_string
from django.utils.encoding import force_text

from debug_toolbar.middleware import (
    DebugToolbarMiddleware as BaseDebugToolbarMiddleware
)

from graphene_django.views import GraphQLView

from .serializers import CallableJSONEncoder

__all__ = ['DebugToolbarMiddleware']


def get_content(response):
    return force_text(response.content, encoding=response.charset)


def set_content(response, content):
    response.content = content

    if response.has_header('Content-Length'):
        response['Content-Length'] = str(len(content))
    return response


def get_payload(request, response, toolbar):
    payload = json.loads(get_content(response), object_pairs_hook=OrderedDict)
    payload['debugToolbar'] = OrderedDict([('panels', OrderedDict())])

    for panel in reversed(toolbar.enabled_panels):
        panel.generate_stats(request, response)

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


class DebugToolbarMiddleware(BaseDebugToolbarMiddleware):

    def process_request(self, request):
        request.is_graphiql = False
        return super().process_request(request)

    def process_view(self, request, view_func, *args):
        request.is_graphiql = hasattr(view_func, 'view_class') and\
            issubclass(view_func.view_class, GraphQLView)

        return super().process_view(request, view_func, *args)

    def process_response(self, request, response):
        is_query = request.is_graphiql and\
            request.content_type == 'application/json'

        toolbar = self.__class__.debug_toolbars.get(
            threading.current_thread().ident, None)

        response = super().process_response(request, response)

        if toolbar is not None and request.is_graphiql and not is_query:
            template = render_to_string('graphiql_debug_toolbar/base.html')
            set_content(response, get_content(response) + template)

        if toolbar is None or not is_query:
            return response

        payload = get_payload(request, response, toolbar)
        set_content(response, json.dumps(payload, cls=CallableJSONEncoder))
        return response
