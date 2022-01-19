from django.contrib.auth import authenticate
from django.core import mail
from django.http import response
from django.test import Client, TestCase
from django.urls import reverse
from post.models import Post
from user.models import User


class Testviews(TestCase):
    def setUp(self):
         self.client = Client()
         user = User.objects.create(username='testuser', password='12345678A!', first_name='Lorenz', last_name='Steidle', email='a@b.de')   
         post = Post.objects.create(title='First Post', description='This is our first Post. ipsum', user=user, content='HTMLField')
        
    def test_createPost(self):
        self.createPost = reverse('create_post')
        response = self.client.get(self.createPost)
        self.assertEqual(response.status_code, 200)

    def test_Postdetails(self):
        self.getPostdetails= reverse('post-detail',args= '1')
        response = self.client.get(self.getPostdetails)
        self.assertEqual(response.status_code, 200)

    def test_deletePost(self):
        #self.deletePost = reverse('delete-post',kwargs= {'post_id':'1', 'user':'1' })
        #response = self.client.get(self.deletePost)
        #self.assertEqual(response.status_code, 404)
        pass    

    def test_viewProfile(self):
        self.viewProfile = reverse('profile')
        response = self.client.get(self.viewProfile)
        self.assertEqual(response.status_code, 200)
    
    def test_register(self):
        self.register = reverse('signup')
        response = self.client.get(self.register)
        self.assertEqual(response.status_code, 200)
    
    def test_home(self):
        self.home = reverse('home')
        response = self.client.get(self.home)
        self.assertEqual(response.status_code, 200)
    
    def test_createComment(self):
       # self.createComment = reverse('create_comment' )
        #response = self.client.get(self.createComment)
        #self.assertEqual(response.status_code, 200)
        pass
    
    def test_send_mail(self):
        mail.send_mail(
            'Titel', 'nachricht',
            'from@example.com', ['to@example.com'],
            fail_silently=False,
        )
        self.assertEqual(len(mail.outbox), 1)
    
    def test_send_mail_title(self):
        mail.send_mail(
            'Titel', 'nachricht',
            'from@example.com', ['to@example.com'],
            fail_silently=False,
        )
        self.assertEqual(mail.outbox[0].subject, 'Titel')


    


    