from django.conf.urls import url, include
from .views import all_threats, add_threat, view_threat, user_upvote, thr_save_curr_page

urlpatterns = [
    url(r'^$', all_threats, name='all_threats'),
    url(r'^(?P<pk>\d+)/$', view_threat, name='view_threat'),
    url(r'^(?P<pk>\d+)/(?P<view>([a-zA-Z]{4}))/$', view_threat, name='view_threat'),
    url(r'^add/$', add_threat, name='add_threat'),    
    url(r'^(?P<pk>\d+)/thr_vote/$', user_upvote, name='user_upvote'),
    url(r'^(?P<pk>\d+)/view/thr_vote/$', user_upvote, name='user_upvote'),
    url(r'^ajax/thr_save_curr_page/$', thr_save_curr_page, name='thr_save_curr_page'),
]