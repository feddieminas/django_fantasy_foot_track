from django.conf.urls import url, include
from .views import all_influences, add_influence

urlpatterns = [
    url(r'^$', all_influences, name='all_influences'),
    url(r'^/add$', add_influence, name='add_influence'),
]