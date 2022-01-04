from django.conf import settings
from django.urls import path, include
from . import views
from .views import downvote, upvote
from django.conf.urls import url
from django.conf.urls.static import static
#from mysite.core import views as core_views

urlpatterns = [
    path('', views.home, name='home'),
    #path('', views.threads, name='home'),
    path("create_post", views.create_post, name='create_post'),
    path('post/<int:pk>', views.post_detail, name='post-detail'),
    path('delete_post/<post_id>/<user>', views.delete_post, name='delete-post'),
    path('<int:post_id>/<user>', views.edit_thread, name='edit_thread'),
    path('create_comment//<post_id>/<user>', views.create_comment, name='create_comment'),
    path('like/<int:pk>', upvote, name= 'like_post'),
    path('dislike/<int:pk>', downvote, name= 'dislike_post'),
    path('search_threads', views.search_threads,name='search_threads'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

