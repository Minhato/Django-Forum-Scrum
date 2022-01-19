from django.test import SimpleTestCase
from django.urls import resolve, reverse
from user.views import signup, profile


class TestUrls(SimpleTestCase):

    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, signup)
    
    def test_signup_url_is_resolved(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)
    

    
