from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from . import views

# All post related urls
urlpatterns = [
    path('', views.home, name='home'),
    path("create_post", views.create_post, name='create_post'),
    path('post/<int:pk>', views.post_detail, name='post-detail'),
    path('delete_post/<post_id>/<user>', views.delete_post, name='delete-post'),
    path('<int:post_id>/<user>', views.edit_post, name='edit_post'),
    path('like/<int:pk>', views.upvote, name= 'like_post'),
    path('dislike/<int:pk>', views.downvote, name= 'dislike_post'),
    path('like_comment/<int:pk>', views.upvote_comment, name= 'like_comment'),
    path('dislike_comment/<int:pk>', views.downvote_comment, name= 'dislike_comment'),
    path('search_post', views.search_post,name='search_post'),
    path('create_comment', views.create_comment, name='create_comment'),
    path('delete_comment/<comment_id>',views.delete_comment, name='delete-comment'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


