from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from . import views
from .views import profile

# All user related urls
urlpatterns = [
    path('register', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



