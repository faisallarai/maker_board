from django.test import TestCase
from django.shortcuts import reverse
from django.core import mail
from django.contrib.auth.models import User

class PasswordResetMailTests(TestCase):

    def setUp(self):
        User.objects.create_user(username='ama', email='ama@example.com', password='12345abcde')
        data = {
            'email': 'ama@example.com'
        }
        url = reverse('password_reset')
        self.response = self.client.post(url, data)
        self.mail = mail.outbox[0]
        
    def test_email_subject(self):
        subject = "[Maker Boards] Please reset your password"
        self.assertEqual(subject, self.mail.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_confirm_url = reverse('password_reset_confirm', kwargs={'token': token, 'uidb64': uid})
        self.assertIn(password_reset_confirm_url, self.mail.body)
        self.assertIn('ama', self.mail.body)
        self.assertIn('ama@example.com', self.mail.body)

    def test_email_to(self):
        self.assertEqual(['ama@example.com',], self.mail.to)