from django.core.paginator import Paginator
from django.http import JsonResponse

from testapp.models import Child


def child_list_view(request):
    per_page = 30

    queryset = Child.objects.select_related('parent')
    count = queryset.count()
    if count == 0:
        return JsonResponse({
            'count': 0,
            'results': [],
            'next_page': None,
            'previous_page': None},
            json_dumps_params={'separators': (',', ':')
        })

    paginator = Paginator(queryset.order_by('id', 'parent_id'), per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    serialized_items = [
        {
            'title': x.title,
            'json_field': x.json_field,
            'long_text': x.long_text,
            'created': x.created,
            'modified': x.modified,
            'parent': {
                'title': x.parent.title,
                'description': x.parent.description,
                'created': x.parent.created,
                'modified': x.parent.modified,
            }
        } for x in page_obj.object_list
    ]

    base_url = f'{request.scheme}://{request.META["HTTP_HOST"]}{request.path}'

    return JsonResponse({
        'count': count,
        'results': serialized_items,
        'next_page': f'{base_url}?page={
            page_obj.next_page_number()}' if page_obj.has_next() else None,
        'previous_page': f'{base_url}?page={
            page_obj.previous_page_number()}' if page_obj.has_previous() else None,
    }, json_dumps_params={'separators': (',', ':')})
