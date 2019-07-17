from django.test import TestCase
from django.shortcuts import reverse
from django.urls import resolve
from django.contrib.auth.models import User

from ..views import board_topics, home, new_topic
from ..models import Board, Topic, Post
from ..forms import NewTopicForm

class HomeTests(TestCase):

    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django Board.')
        url = reverse('home')
        self.response = self.client.get(url)


    def test_home_view_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)

    def test_home_view_contains_links_to_board_topics(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk })
        self.assertContains(self.response, f'href="{board_topics_url}"')
        


class BoardTopicsTests(TestCase):

    def setUp(self):
        Board.objects.create(name='Django', description='Django Board')

    def test_board_topics_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_topics_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolve_to_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEqual(view.func, board_topics)

    def test_board_topics_view_contains_link_back_to_home_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        home_url = reverse('home')
        self.assertContains(response, f'href="{home_url}"')

    def test_board_topics_contains_new_topic_link(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})

        self.assertContains(response, f'href="{new_topic_url}"')



class NewTopicTests(TestCase):

    def setUp(self):
        Board.objects.create(name='Django', description='Django Board.')
        User.objects.create_user(username='john', email='john@doe.com', password='123') 

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1 })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resloves_to_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_points_to_topic_template(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        
        self.assertTemplateUsed(response, 'boards/new_topic.html')

    def test_new_topic_view_contains_link_back_to_board_topics(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})

        self.assertContains(response, f'href="{board_topics_url}"')


    def test_form_csrf(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_form_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test Title',
            'message': 'Test Message'
        }

        self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_form_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_new_topic_empty_form_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_new_topic_invalid_data_should_contain_errors(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {}
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_contains_form(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, NewTopicForm)

        
