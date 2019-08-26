from django.conf.urls import url, include
from .views import all_creativities, add_creativity, view_creativity, user_upvote, cre_save_curr_page

urlpatterns = [
    url(r'^$', all_creativities, name='all_creativities'),
    url(r'^(?P<pk>\d+)/$', view_creativity, name='view_creativity'),
    url(r'^(?P<pk>\d+)/(?P<view>([a-zA-Z]{4}))/$', view_creativity, name='view_creativity'),
    url(r'^add/$', add_creativity, name='add_creativity'),    
    url(r'^(?P<pk>\d+)/cre_vote/$', user_upvote, name='user_upvote'),
    url(r'^(?P<pk>\d+)/view/cre_vote/$', user_upvote, name='user_upvote'),
    url(r'^ajax/cre_save_curr_page/$', cre_save_curr_page, name='cre_save_curr_page'),
]