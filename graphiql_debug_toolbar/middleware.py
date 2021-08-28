import json
from collections import OrderedDict

from django.template.loader import render_to_string
from django.utils.encoding import force_str

from debug_toolbar.middleware import _HTML_TYPES
from debug_toolbar.middleware import DebugToolbarMiddleware as BaseMiddleware
from debug_toolbar.toolbar import DebugToolbar
from graphene_django.views import GraphQLView

from .serializers import CallableJSONEncoder

__all__ = ["DebugToolbarMiddleware"]


def set_content_length(response):
    if response.has_header("Content-Length"):
        response["Content-Length"] = str(len(response.content))


def get_payload(request, response, toolbar):
    content = force_str(response.content, encoding=response.charset)
    payload = json.loads(content, object_pairs_hook=OrderedDict)
    payload["debugToolbar"] = OrderedDict([("panels", OrderedDict())])

    for panel in reversed(toolbar.enabled_panels):
        if panel.panel_id == "TemplatesPanel":
            continue

        if panel.has_content:
            title = panel.title
        else:
            title = None

        payload["debugToolbar"]["panels"][panel.panel_id] = {
            "title": title,
            "subtitle": panel.nav_subtitle,
        }

    payload["debugToolbar"]["storeId"] = toolbar.store_id
    return payload


_store = DebugToolbar.store


class DebugToolbarMiddleware(BaseMiddleware):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.store_id = None

    def process_view(self, request, view_func, *args):
        if (
            hasattr(view_func, "view_class")
            and issubclass(view_func.view_class, GraphQLView)
            and view_func.view_initkwargs.get("graphiql")
        ):
            request._graphiql = True

    def store(self):
        def decorator(toolbar):
            _store(toolbar)
            self.store_id = toolbar.store_id

        return decorator

    def __call__(self, request):
        DebugToolbar.store = self.store()
        response = super().__call__(request)
        DebugToolbar.store = _store

        content_type = response.get("Content-Type", "").split(";")[0]
        is_html = content_type in _HTML_TYPES
        is_graphiql = getattr(request, "_graphiql", False)

        if is_html and is_graphiql and response.status_code == 200:
            template = render_to_string("graphiql_debug_toolbar/base.html")
            response.write(template)
            set_content_length(response)

        if (
            is_html
            or self.store_id is None
            or not (is_graphiql and content_type == "application/json")
        ):
            return response

        toolbar = DebugToolbar.fetch(self.store_id)
        payload = get_payload(request, response, toolbar)
        response.content = json.dumps(payload, cls=CallableJSONEncoder)
        set_content_length(response)
        return response
