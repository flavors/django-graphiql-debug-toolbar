import json
from unittest.mock import PropertyMock, patch

from django.http import HttpResponse, JsonResponse
from django.test import RequestFactory, testcases

from graphene_django.views import GraphQLView

from graphiql_debug_toolbar.middleware import DebugToolbarMiddleware


class MiddlewareTests(testcases.TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = DebugToolbarMiddleware()
        self.view_func = GraphQLView.as_view()

    @patch('debug_toolbar.middleware.show_toolbar', return_value=True)
    def test_graphiql(self, *args):
        request = self.factory.get('/')

        self.middleware.process_request(request)
        self.middleware.process_view(request, self.view_func, (), {})

        response_mock = HttpResponse()
        response = self.middleware.process_response(request, response_mock)

        self.assertIn(b'debug-toolbar-parse', response.content)

    @patch('debug_toolbar.middleware.show_toolbar', return_value=True)
    @patch('debug_toolbar.panels.Panel.enabled', new_callable=PropertyMock)
    def test_query(self, panel_enabled_mock, *args):
        panel_enabled_mock.return_value = True
        request = self.factory.post('/', content_type='application/json')

        self.middleware.process_request(request)
        self.middleware.process_view(request, self.view_func, (), {})

        response_mock = JsonResponse({'data': None})
        response = self.middleware.process_response(request, response_mock)

        payload = json.loads(response.content.decode('utf-8'))
        panel_enabled_mock.assert_called_with()

        self.assertIn('data', payload)
        self.assertIn('storeId', payload['debugToolbar'])

    def test_hidden_toolbar(self):
        request = self.factory.get('/')

        self.middleware.process_request(request)

        response_mock = HttpResponse('.')
        response = self.middleware.process_response(request, response_mock)

        self.assertEqual(b'.', response.content)
