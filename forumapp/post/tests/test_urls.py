from django.test import SimpleTestCase
from django.urls import resolve, reverse
from post.views import (create_comment, create_post, delete_comment,
                        delete_post, edit_post, home, post_detail, search_post)


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_create_post_url_is_resolved(self):
        url = reverse('create_post')
        self.assertEquals(resolve(url).func, create_post)

    def test_edit_post_url_is_resolved(self):
        pk =1
        url = reverse('edit_post', args=[pk,'Lorenz Steidle'])
        self.assertEquals(resolve(url).func, edit_post)

    def test_search_posts_url_is_resolved(self):
        url = reverse('search_post')
        self.assertEquals(resolve(url).func, search_post)
    
    #def test_delete_post_url_is_resolved(self):
    #    pk =1
    #    url = reverse('delete_post', args=[pk,'Lorenz Steidle'])
    #    self.assertEquals(resolve(url).func, delete_post)

    def test_create_comment_url_is_resolved(self):
        url = reverse('create_comment')
        self.assertEquals(resolve(url).func, create_comment)

    #def test_delete_comment_url_is_resolved(self):
    #    id=1
    #    url = reverse('delete_comment', args=[id])
    #    self.assertEquals(resolve(url).func, delete_comment)
