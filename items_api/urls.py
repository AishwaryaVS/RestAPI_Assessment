# todo/todo_api/urls.py : API urls.py
# from django.conf.urls import re_path
from django.urls import path, include, re_path
from .views import (
    
    ItemsListApiView

)

urlpatterns = [
    path('api', ItemsListApiView.as_view(), name='items-list')
]