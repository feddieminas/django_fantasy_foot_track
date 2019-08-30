"""fantasyfoottrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include 
from django.contrib import admin
from django.urls import path
from accounts import urls as urls_accounts
from accounts.views import index
from influence import urls as urls_influence
from creativity import urls as urls_creativity
from threat import urls as urls_threat
from donate import urls as urls_donate
from graph import urls as urls_graph
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'), 
    path('accounts/', include(urls_accounts)),
    path('influences/', include(urls_influence)),
    path('creativities/', include(urls_creativity)),    
    path('threats/', include(urls_threat)),
    path('donate/', include(urls_donate)),
    path('graph/', include(urls_graph)),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT }),
]
