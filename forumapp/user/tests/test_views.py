
from django.contrib.auth import authenticate
from django.http import response
from django.test import TestCase
from django.test import Client
from user.models import Post
from django.contrib.auth.models import User
from django.urls import reverse

class Testviews(TestCase):
    def setUp(self):
         self.client = Client()
         user = User.objects.create(username='testuser', password='12345678A!', first_name='Lorenz', last_name='Steidle', email='a@b.de')   
         post = Post.objects.create(title='First Post', description='This is our first Post. ipsum', user=user, content='HTMLField')
         self.createPost = reverse('create_post')
         self.getPostdetails= reverse('post-detail',args= '1')
         self.deletePost = reverse('delete-post',kwargs= {'post_id':'1', 'user':'1' })
        
    def test_createPost(self):
        response = self.client.get(self.createPost)
        self.assertEqual(response.status_code, 200)

    def test_Postdetails(self):
        response = self.client.get(self.getPostdetails)
        self.assertEqual(response.status_code, 200)

    def test_deletePost(self):
        #response = self.client.get(self.deletePost)
        #self.assertEqual(response.status_code, 200)
        pass

    