from django.db import models
from django.utils import timezone


class Parent(models.Model):

    title = models.CharField(max_length=64)
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)


class Child(models.Model):

    parent = models.ForeignKey('Parent', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=64)
    json_field = models.JSONField()
    long_text = models.TextField()
