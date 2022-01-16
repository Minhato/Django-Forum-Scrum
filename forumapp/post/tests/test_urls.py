from django.test import SimpleTestCase
from django.urls import resolve, reverse
from post.views import home, create_post

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_create_post_url_is_resolved(self):
        url = reverse('create_post')
        self.assertEquals(resolve(url).func, create_post)