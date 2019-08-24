from django.conf.urls import url, include
from .views import all_influences, add_influence, view_influence, user_upvote, save_curr_page

urlpatterns = [
    url(r'^$', all_influences, name='all_influences'),
    url(r'^(?P<pk>\d+)/$', view_influence, name='view_influence'),
    url(r'^(?P<pk>\d+)/(?P<view>([a-zA-Z]{4}))/$', view_influence, name='view_influence'),
    url(r'^add/$', add_influence, name='add_influence'),    
    url(r'^(?P<pk>\d+)/inf_vote/$', user_upvote, name='user_upvote'),
    url(r'^(?P<pk>\d+)/view/inf_vote/$', user_upvote, name='user_upvote'),
    url(r'^ajax/save_curr_page/$', save_curr_page, name='save_curr_page'),
]