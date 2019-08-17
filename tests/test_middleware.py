import json
from unittest.mock import Mock, PropertyMock, patch

from django.http import HttpResponse, JsonResponse
from django.test import RequestFactory, testcases

from graphene_django.views import GraphQLView

from graphiql_debug_toolbar.middleware import DebugToolbarMiddleware


class DebugToolbarMiddlewareTests(testcases.TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.view_func = GraphQLView.as_view()

    @patch('debug_toolbar.middleware.show_toolbar', return_value=True)
    def test_graphiql(self, show_toolbar_mock):
        request = self.request_factory.get('/')
        http_response = HttpResponse()
        http_response['Content-Length'] = 0
        get_response_mock = Mock(return_value=http_response)

        middleware = DebugToolbarMiddleware(get_response_mock)
        middleware.process_view(request, self.view_func, (), {})
        response = middleware(request)

        show_toolbar_mock.assert_called_with(request)
        self.assertGreater(int(response['Content-Length']), 0)
        self.assertIn(b'djGraphiQLDebug', response.content)

    @patch('debug_toolbar.panels.Panel.enabled', new_callable=PropertyMock)
    def test_query(self, panel_enabled_mock):
        panel_enabled_mock.return_value = True

        request = self.request_factory.post('/')
        get_response_mock = Mock(return_value=JsonResponse({'data': None}))

        middleware = DebugToolbarMiddleware(get_response_mock)
        middleware.process_view(request, self.view_func, (), {})

        response = middleware(request)
        payload = json.loads(response.content.decode('utf-8'))

        panel_enabled_mock.assert_called_with()
        self.assertIn('data', payload)
        self.assertIn('storeId', payload['debugToolbar'])

    def test_hidden_toolbar(self):
        request = self.request_factory.post('/')
        get_response_mock = Mock(return_value=HttpResponse('.'))
        middleware = DebugToolbarMiddleware(get_response_mock)
        response = middleware(request)

        self.assertEqual(b'.', response.content)
