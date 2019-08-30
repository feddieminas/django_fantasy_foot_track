from django.conf.urls import url, include
from django.urls import path
from accounts.views import index, logout, login, registration, user_profile
from accounts import url_reset 

urlpatterns = [
    path('logout/', logout, name="logout"), 
    path('login/', login, name="login"),
    path('register/', registration, name="registration"),
    path('profile/', user_profile, name="profile"),
    path('password-reset/', include(url_reset)),
]

