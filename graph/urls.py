from django.conf.urls import url
from .views import show_graph

urlpatterns = [
    url(r'^$', show_graph, name='show_graph')
    ]