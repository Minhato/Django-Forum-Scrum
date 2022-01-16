from django.http import response
from django.test import TestCase
from post.models import Post
from django.contrib.auth.models import User

class TestModel(TestCase):
    @classmethod
    def setupTestData(cls):
        user = User.objects.create(username='testuser', password='12345678A!', first_name='Lorenz', last_name='Steidle', email='a@b.de')   
        print(user)
        post = Post.objects.create(title='First Post', description='This is our first Post. ipsum', user=user, content='HTMLField')
        print(post)

    #def test_board_name(self):
    #    board_name = Post.objects.filter(id=4)
    #    field_label = board_name._meta.get_field('title').verbose_name
    #    self.assertEqual(field_label, 'title')
    
  #  def test_board_description(self):
   #     board_description = Post.objects.get(id=1)
    #    field_label = board_description._meta.get_field('description').verbose_name
     #   self.assertEqual(field_label, 'description')