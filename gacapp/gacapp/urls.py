'''
URL configuration for gacapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import  function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
'''
from django.contrib import admin
from django.urls import path
from gacdsl import views
#from gacdsl.views import views
#import sys
#sys.path.insert(0, '/home/c/cq87810/spdonates/public_html/gacapp/gacapp')
#from views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/user', views.get_authenticated_user, name='get_authenticated_user'),
    path('auth/streamers', views.authenticated_user_streamers, name='streramers_page'),
    path('oauth2', views.home, name='oauth2'),
    path('oauth2/login', views.ds_login, name='oauth2_login'),
    path('oauth2/login/redirect', views.ds_login_redirect, name='oauth2_login_redirect'),
    path('input/', views.input_view, name='input'),
    path('', views.mainp, name='main_page'),
    path('webhook', views.webhook_receiver, name='webhook_receiver'),
    path('donates', views.render_a_donates, name='render_donates_page')
]
