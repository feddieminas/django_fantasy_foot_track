from django.conf.urls import url
from django.urls import path, re_path
from .views import all_creativities, add_creativity, view_creativity, cre_user_upvote, cre_save_curr_page

urlpatterns = [
    path('', all_creativities, name='all_creativities'),
    path('add/', add_creativity, name='add_creativity'),
    path('<pk>/', view_creativity, name='view_creativity'),
    re_path(r'^(?P<pk>\d+)/(?P<view>([a-zA-Z]{4}))/$', view_creativity, name='view_creativity'),
    path('<pk>/cre_vote/', cre_user_upvote, name='cre_user_upvote'),
    path('<pk>/view/cre_vote/', cre_user_upvote, name='cre_user_upvote'),    
    re_path(r'^ajax/cre_save_curr_page/$', cre_save_curr_page, name='cre_save_curr_page'),
]