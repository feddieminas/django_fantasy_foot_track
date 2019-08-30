from django.conf.urls import url
from django.urls import path
from .views import donate

urlpatterns = [
    path('', donate, name='donate'),
    ]    