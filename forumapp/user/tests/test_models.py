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


"""     def test_post_title(self):
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
        self.assertEqual(field_label, 'parent') """
