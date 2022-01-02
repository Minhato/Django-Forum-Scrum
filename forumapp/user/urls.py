from django.conf import settings
from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf.urls.static import static
#from mysite.core import views as core_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.signup, name='signup'),
]

