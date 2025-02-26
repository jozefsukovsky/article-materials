from django.contrib import admin
from django.urls import path
from django.conf import settings

from account.views import demo_view, logout_view

urlpatterns = []

if settings.ENVIRONMENT == 'admin':
    urlpatterns.append(path('admin/', admin.site.urls))
else:
    urlpatterns.append(path('', demo_view, name='demo_view'))
    urlpatterns.append(path('logout/', logout_view, name='logout_view'))
