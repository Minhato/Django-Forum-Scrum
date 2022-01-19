from xmlrpc.client import DateTime
from django.test import TestCase
from post.models import Comment, Post
from user.models import User


class TestModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', password='12345678A!', first_name='Lorenz', last_name='Steidle', email='a@b.de') 
        post = Post.objects.create(title='First Post', description='This is our first Post. ipsum', user=user, content='HTMLField')
        Comment.objects.create(post=post, user=user, comment_content='First Comment', date= DateTime, votes=1, parent= None)

    def test_post_title(self):
        post_title = Post.objects.get(id=1)
        field_label = post_title._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_post_description(self):
        board_description = Post.objects.get(id=1)
        field_label = board_description._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_comment_content(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('comment_content').verbose_name
        self.assertEqual(field_label, 'comment content')

    def test_comment_date(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'date')

    def test_comment_votes(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('votes').verbose_name
        self.assertEqual(field_label, 'votes')

    def test_comment_parent(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('parent').verbose_name
        self.assertEqual(field_label, 'parent')
