from django.test import TestCase
from django.shortcuts import reverse
from django.urls import resolve
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from ..views import signup
from ..forms import SignUpForm


class SignupTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_sign_up_view_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_sign_up_view_points_to_correct_template(self):
        self.assertTemplateUsed(self.response, 'accounts/signup.html')

    def test_sign_up_url_resolves_to_sign_up_view(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(view.func, signup)

    def test_csrf_token_in_sign_up_view(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_sign_up_view_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        self.assertContains(self.response, "<input", 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

class SignupValidDataTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'admingali',
            'password1': 'abcde1234',
            'password2': 'abcde1234'
        }

        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class SignupValidDataTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        data = {}
        self.response = self.client.post(url, data)

    def test_no_redirection(self):
        ''' No redirection means data is invalid'''
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_no_account_created(self):
        self.assertFalse(User.objects.exists())