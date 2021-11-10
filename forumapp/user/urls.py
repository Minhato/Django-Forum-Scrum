from django.urls import path, include
from . import views
from django.conf.urls import url
#from mysite.core import views as core_views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.signup, name='signup'),
    #path('login', views.login, name='login'),  
]

#test
##asdasdas
