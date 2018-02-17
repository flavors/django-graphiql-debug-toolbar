import json

from django.test import testcases

from graphiql_debug_toolbar import serializers


class SerializersTests(testcases.TestCase):

    def test_callable_json_encoder(self):
        result = json.dumps({
            '.': '.',
            '..': lambda: '..',
        }, cls=serializers.CallableJSONEncoder)

        self.assertEqual(result, '{".": ".", "..": ".."}')
