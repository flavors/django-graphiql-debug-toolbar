import json
import threading
from collections import OrderedDict

from django.template.loader import render_to_string
from django.utils.encoding import force_text

from debug_toolbar import middleware
from graphene_django.views import GraphQLView

from .serializers import CallableJSONEncoder

__all__ = ['DebugToolbarMiddleware']


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


class DebugToolbarMiddleware(middleware.DebugToolbarMiddleware):

    def process_request(self, request):
        request.is_graphql_view = False
        return super().process_request(request)

    def process_view(self, request, view_func, *args):
        request.is_graphql_view = hasattr(view_func, 'view_class') and\
            issubclass(view_func.view_class, GraphQLView)

        return super().process_view(request, view_func, *args)

    def process_response(self, request, response):
        toolbar = type(self).debug_toolbars.get(
            threading.current_thread().ident, None)

        response = super().process_response(request, response)
        content_type = response.get('Content-Type', '').split(';')[0]
        html_type = content_type in middleware._HTML_TYPES

        if (response.status_code == 200 and
                toolbar is not None and
                request.is_graphql_view and
                html_type):

            template = render_to_string('graphiql_debug_toolbar/base.html')
            response.write(template)
            set_content_length(response)

        if toolbar is None or html_type or not (
                request.is_graphql_view and
                request.content_type == 'application/json'):
            return response

        payload = get_payload(request, response, toolbar)
        response.content = json.dumps(payload, cls=CallableJSONEncoder)
        set_content_length(response)
        return response
