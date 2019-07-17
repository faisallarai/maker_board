from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.forms

class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        '''
        User tries to access `password_change` view without being logged in. 
        The user is expected to be redirected back to the log in view
        '''
        url = reverse('password_change')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')

class PasswordChangeTestCase(TestCase):

    def setUp(self, data={}):
        self.user = User.objects.create_user(username='ama', email='ama@example.com', password='abcde12345')
        self.url = reverse('password_change')
        self.client.login(username=self.user.username, password=self.user.password)
        self.response = self.client.post(self.url, data)

class SuccessfulPasswordChangeTests(PasswordChangeTestCase):

    def setUp(self):
        super().setUp({
            'old_password': 'abcde12345',
            'new_password1': 'hgtion12345',
            'new_password2': 'hgtion12345'
        })

    def test_redirection(self):
        '''
        A valid form submission should redirect the user 
        '''
        password_change_done_url = reverse('password_change_done')
        self.assertRedirects(self.response, password_change_done_url)

    def test_password_changed(self):
        '''
        Refresh the user instance from the database to get the 
        hash updated by the change password view
        '''
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('hgtion12345'))

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context, after a successful sign up.
        '''
        home_url = reverse('home')
        response = self.client.get(home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)