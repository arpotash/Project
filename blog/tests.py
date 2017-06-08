from django.test import TestCase, Client
from .models import Post,Comment 
from django.utils import timezone
from django.core.urlresolvers import reverse
from .forms import *
#from django.utils import unittest


class PublicViewTest(TestCase):
    def test_anonymous_can_access_localhost(self):
        url = Client()
        response = url.get('/post/8/')
        self.assertEqual(response.status_code, 200)#Code 200 -  because in this project we using the template - unauthorized.html 



class AvailabilityofLocalhost(TestCase):

    def test_homepage_available(self):
        c = Client()
        response = c.get('/')
        self.assertEquals(response.status_code, 200)


class Setup_Class(TestCase):

    def setUp(self):
        self.Post = Post.objects.create(title = "new post", text="new text")

class Post_Form_Test(TestCase):

    def test_PostForm_valid(self):
        form = PostForm(data={'title': "some title", 'text': "some text"})
        self.assertTrue(form.is_valid())


    def test_PostForm_invalid(self):
        form = PostForm(data={'title': "", 'text': ""})




class Setup_Class(TestCase):

    def setUp(self):
        self.Comment = Comment.objects.create(name = "name", email="email@email.com", body = "Comment")
