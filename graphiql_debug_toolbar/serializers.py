from django.core.serializers.json import DjangoJSONEncoder


class CallableJSONEncoder(DjangoJSONEncoder):

    def default(self, obj):
        if callable(obj):
            return obj()
        return super().default(obj)
