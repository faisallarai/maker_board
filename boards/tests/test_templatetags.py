from django.test import TestCase
from django import forms
from django.contrib.auth.models import User

from ..templatetags.form_tags import field_type, input_class

class ExampleForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

class FieldTypeTests(TestCase):
    def test_field_widget_type(self):
        form = ExampleForm()
        self.assertEqual('TextInput', field_type(form['username']))
        self.assertEqual('PasswordInput', field_type(form['password']))

class InuptClassTests(TestCase):

    def test_unbound_field_initial_state(self):
        form = ExampleForm() # unbound form
        self.assertEqual('form-control ', input_class(form['username']))

    def test_valid_bound_field(self):
        form = ExampleForm({'username':'ama', 'password':'123456'}) # bound form (field + data)
        self.assertEqual('form-control valid', input_class(form['username']))
        self.assertEqual('form-control ', input_class(form['password']))

    def test_invalid_bound_field(self):
        form = ExampleForm({'username': '', 'password': '123456'})
        self.assertEqual('form-control invalid', input_class(form['username']))
