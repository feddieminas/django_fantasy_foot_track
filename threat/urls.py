from django.conf.urls import url
from django.urls import path, re_path
from .views import all_threats, add_threat, view_threat, thr_user_upvote, thr_save_curr_page

urlpatterns = [
    path('', all_threats, name='all_threats'),
    path('add/', add_threat, name='add_threat'),  
    path('<pk>/', view_threat, name='view_threat'),
    re_path(r'^(?P<pk>\d+)/(?P<view>([a-zA-Z]{4}))/$', view_threat, name='view_threat'),
    path('<pk>/thr_vote/', thr_user_upvote, name='thr_user_upvote'),
    path('<pk>/view/thr_vote/', thr_user_upvote, name='thr_user_upvote'),    
    re_path(r'^ajax/thr_save_curr_page/$', thr_save_curr_page, name='thr_save_curr_page'),
]