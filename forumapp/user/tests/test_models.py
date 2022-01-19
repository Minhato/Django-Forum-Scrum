from django.http import response
from django.test import TestCase
from post.models import Comment, Post
from user.models import Profile, User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='testuser', password='12345678A!', first_name='Lorenz', last_name='Steidle', email='a@b.de')
        #post = Post.objects.create(title='First Post', description='This is our first Post. ipsum', user=user, content='HTMLField')
        #comment = Comment.objects.create(post=post, user=user, comment_content='First Comment', date= None, votes=1, parent= None)

    def test_username_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')

    def test_password_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('password').verbose_name
        self.assertEqual(field_label, 'password')

    def test_first_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email address')

    #def testdepartment_label(self):
    #    user = User.objects.get(id=1)
    #    field_label = user._meta.get_field('department').verbose_name
    #    print(field_label)
    #    self.assertEqual(field_label, 'department')
