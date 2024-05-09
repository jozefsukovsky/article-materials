from django.urls import path
from testapp.views import child_list_view

urlpatterns = [
    path('children', child_list_view)
]
