from django.conf.urls import url
from django.urls import path
from .views import show_graph

urlpatterns = [
    path('', show_graph, name='show_graph'),
    ]    