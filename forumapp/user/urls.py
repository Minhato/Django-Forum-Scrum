from django.urls import path, include
from . import views
from .views import post_detail, profile
from django.conf.urls import url
#from mysite.core import views as core_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.signup, name='signup'),
    #path('', views.threads, name='home'),
    path("create_post", views.create_post, name='create_post'),
    path('post/<int:pk>', views.post_detail, name='post-detail'),
    path('delete_post/<post_id>/<user>', views.delete_post, name='delete-post'),
    path('profile', views.profile, name='profile')
    #path('login', views.login, name='login'),  
]

