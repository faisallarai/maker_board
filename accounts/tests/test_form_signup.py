from django.test import TestCase

from ..forms import SignUpForm

class SignUpFormTest(TestCase):

    def test_form_has_fields(self):
        form = SignUpForm()
        expected_fields = ['username', 'email', 'password1', 'password2']
        actual_fields = list(form.fields)
        self.assertSequenceEqual(actual_fields, expected_fields)
