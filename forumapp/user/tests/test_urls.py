from django.test import SimpleTestCase
from django.urls import resolve, reverse
from user.views import  signup

class TestUrls(SimpleTestCase):

   # def test_home_url_is_resolved(self):
   #     url = reverse('home')
   #     self.assertEquals(resolve(url).func, home)

    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, signup)
    
   # def test_create_post_url_is_resolved(self):
   #     url = reverse('create_post')
   #     self.assertEquals(resolve(url).func, create_post)