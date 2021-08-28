import json
from unittest.mock import Mock, patch

from django.http import HttpResponse, JsonResponse
from django.test import RequestFactory, testcases

from graphene_django.views import GraphQLView

from graphiql_debug_toolbar.middleware import DebugToolbarMiddleware


class DebugToolbarMiddlewareTests(testcases.TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.view_func = GraphQLView.as_view(graphiql=True)
        self.middleware = DebugToolbarMiddleware

    def test_graphiql(self):
        request = self.request_factory.get("/")
        http_response = HttpResponse(headers={"Content-Length": 0})
        get_response_mock = Mock(return_value=http_response)

        middleware = self.middleware(get_response_mock)
        middleware.process_view(request, self.view_func)
        response = middleware(request)

        self.assertGreater(int(response["Content-Length"]), 0)
        self.assertIn(b"parse.js", response.content)

    @patch("debug_toolbar.middleware.get_show_toolbar", return_value=lambda r: True)
    def test_query(self, get_show_toolbar_mock):
        request = self.request_factory.post("/")
        get_response_mock = Mock(return_value=JsonResponse({"data": None}))

        middleware = self.middleware(get_response_mock)
        middleware.process_view(request, self.view_func, (), {})

        response = middleware(request)
        payload = json.loads(response.content.decode("utf-8"))

        get_show_toolbar_mock.assert_called_once_with()
        self.assertIn("data", payload)
        self.assertIn("storeId", payload["debugToolbar"])

    def test_process_unknown_view(self):
        request = self.request_factory.post("/")
        get_response_mock = Mock(return_value=HttpResponse())

        middleware = self.middleware(get_response_mock)
        middleware.process_view(request, None)

        self.assertFalse(hasattr("request", "_graphiql"))
