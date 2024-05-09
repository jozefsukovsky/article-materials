import orjson

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse


from testapp.test_data import test_data


class OrjsonResponse(HttpResponse):
    def __init__(
        self,
        data,
        _encoder=DjangoJSONEncoder,
        safe=True,
        **kwargs,
    ):
        if safe and not isinstance(data, dict):
            raise TypeError(
                "In order to allow non-dict objects to be serialized set the "
                "safe parameter to False."
            )
        kwargs.setdefault("content_type", "application/json")
        data = orjson.dumps(data)
        super().__init__(content=data, **kwargs)


def child_list_view(_request):
    return OrjsonResponse(test_data)
