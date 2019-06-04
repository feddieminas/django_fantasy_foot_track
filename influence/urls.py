from django.conf.urls import url, include
from .views import all_influences, add_influence, view_influence, add_influ_comment, user_upvote

urlpatterns = [
    url(r'^$', all_influences, name='all_influences'),
    url(r'^(?P<pk>\d+)/$', view_influence, name='view_influence'),
    url(r'^(?P<pk>\d+)/(?P<view>([a-zA-Z]{4}))/$', view_influence, name='view_influence'),
    url(r'^add$', add_influence, name='add_influence'),    
    url(r'^(?P<pk>\d+)/add_comment/$', add_influ_comment, name='add_influ_comment'),
    url(r'^(?P<pk>\d+)/bug_vote/$', user_upvote, name='user_upvote'),
    url(r'^(?P<pk>\d+)/view/bug_vote/$', user_upvote, name='user_upvote'),
]