from django.http import JsonResponse

from testapp.test_data import test_data


def child_list_view(_request):
    return JsonResponse(test_data, json_dumps_params={'separators': (',', ':')})
