from django.conf.urls import url
from django.urls import path, re_path
from .views import all_influences, add_influence, view_influence, user_upvote, save_curr_page

urlpatterns = [
    path('', all_influences, name='all_influences'),
    path('add/', add_influence, name='add_influence'), 
    path('<pk>/', view_influence, name='view_influence'),
    re_path(r'^(?P<pk>\d+)/(?P<view>([a-zA-Z]{4}))/$', view_influence, name='view_influence'),
    path('<pk>/inf_vote/', user_upvote, name='user_upvote'),
    path('<pk>/view/inf_vote/', user_upvote, name='user_upvote'),    
    re_path(r'^ajax/save_curr_page/$', save_curr_page, name='save_curr_page'),
]