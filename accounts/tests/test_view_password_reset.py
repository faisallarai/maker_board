from django.test import TestCase
from django.urls import resolve
from django.core import mail
from django.shortcuts import reverse
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

class PasswordResetTests(TestCase):

    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/reset/')
        self.assertEqual(view.func.view_class, PasswordResetView)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'accounts/password_reset.html')

    def test_contains_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_forms(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs_available(self):
        ''' 
        The view must contain csrf and email 
        '''
        self.assertContains(self.response, '<input', 2) # includind csrf_token
        self.assertContains(self.response, 'type="email"', 1)

class SuccessfulPasswordResetTests(TestCase):

    def setUp(self):
        '''
        Create a user to test reset password with
        '''
        email = 'ama@example.com'
        User.objects.create_user(username='ama', email=email, password='123456abcde')
        url = reverse('password_reset')
        data = {
            'email': email
        }
        self.response = self.client.post(url, data)

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to `password_reset_done` view
        '''
        password_reset_done_url = reverse('password_reset_done')
        self.assertRedirects(self.response, password_reset_done_url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))

class InvalidPasswordResetTests(TestCase):

    def setUp(self):
        url = reverse('password_reset')
        data = {
            'email': 'ama@example.com'
        }
        self.response = self.client.post(url, data)

    def test_redirection(self):
        '''
        An invalid email should still redirect the user to `password_reset_done` view
        '''
        password_reset_done_url = reverse('password_reset_done')
        self.assertRedirects(self.response, password_reset_done_url)

    def test_no_reset_email(self):
        self.assertEqual(0, len(mail.outbox))

class PasswordResetDoneTests(TestCase):

    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/reset/done/')
        self.assertEqual(view.func.view_class, PasswordResetDoneView)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'accounts/password_reset_done.html')

class PasswordResetConfirmTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='ama', email='ama@example.com', password='abcde1245')
        self.token = default_token_generator.make_token(user)
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))

        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f'/accounts/reset/{self.uid}/{self.token}/')
        self.assertEqual(view.func.view_class, PasswordResetConfirmView)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'accounts/password_reset_confirm.html')

    def test_contains_forms(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_contains_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs_available(self):
        '''
        The view must contain csrf, new password and new password confirmation
        '''
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)

class InvalidPasswordResetConfirmTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='ama', email='ama@example.com', password='12345abcde')
        self.token = default_token_generator.make_token(user)
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))

        '''
        Invalidate the token by changing the password
        '''
        user.set_password('abcde12345')
        user.save()

        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_html(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, f'href="{password_reset_url}"')

class PasswordResetCompleteTests(TestCase):

    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/reset/complete/')
        self.assertEqual(view.func.view_class, PasswordResetCompleteView)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'accounts/password_reset_complete.html')

    def test_html(self):
        login_url = reverse('login')
        self.assertContains(self.response, 'You have successfully changed your password!')
        self.assertContains(self.response, f'href="{login_url}"')