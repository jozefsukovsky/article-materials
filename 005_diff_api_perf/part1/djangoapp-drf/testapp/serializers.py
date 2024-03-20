from testapp.models import Child, Parent
from rest_framework import serializers


class ParentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parent
        fields = ['title', 'description', 'created', 'modified']


class ChildSerializer(serializers.ModelSerializer):

    parent = ParentSerializer()

    class Meta:
        model = Child
        fields = ['parent', 'created', 'modified', 'title', 'json_field', 'long_text']
