from rest_framework import viewsets

from testapp.models import Child
from testapp.serializers import ChildSerializer


class ChildViewSet(viewsets.ModelViewSet):

    queryset = Child.objects.select_related('parent').order_by('id', 'parent_id')
    serializer_class = ChildSerializer
