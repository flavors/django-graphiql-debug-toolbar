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
    def test_graphiql_introspection_query(self, panel_enabled_mock):
        panel_enabled_mock.return_value = True

        def _test_request():
            request = self.request_factory.post('/')
            get_response_mock = Mock(return_value=JsonResponse({'data': { '__schema': ''}}))

            middleware = DebugToolbarMiddleware(get_response_mock)
            middleware.process_view(request, self.view_func, (), {})

            response = middleware(request)
            payload = json.loads(response.content.decode('utf-8'))

            panel_enabled_mock.assert_called_with()
            self.assertIn('data', payload)
            return payload

        with self.settings(GRAPHIQL_DEBUG_TOOLBAR_INTROSPECTIONS=False):
            payload = _test_request()
            self.assertNotIn('debugToolbar', payload)

        with self.settings(GRAPHIQL_DEBUG_TOOLBAR_INTROSPECTIONS=True):
            payload = _test_request()
            self.assertIn('debugToolbar', payload)

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

    @patch('graphiql_debug_toolbar.middleware.get_show_toolbar')
    def test_hidden_toolbar(self, show_toolbar_mock):
        show_toolbar_mock.return_value = lambda request: False

        request = self.request_factory.post('/')
        get_response_mock = Mock(return_value=HttpResponse())

        middleware = DebugToolbarMiddleware(get_response_mock)
        middleware.process_view(request, self.view_func, (), {})
        response = middleware(request)

        show_toolbar_mock.assert_called_with()
        self.assertNotIn(b'djGraphiQLDebug', response.content)

    def test_process_unknown_view(self):
        request = self.request_factory.post('/')
        get_response_mock = Mock(return_value=HttpResponse())

        middleware = DebugToolbarMiddleware(get_response_mock)
        middleware.process_view(request, None, (), {})

        self.assertFalse(hasattr('request', '_graphql_view'))
