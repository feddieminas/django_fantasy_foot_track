""" Accounts Test Forms 
"""

from django.test import TestCase
from .forms import UserLoginForm, UserRegistrationForm, FilterView
from django.contrib.auth.models import User

class TestAccountsForms(TestCase):
    def test_login_field_required(self):
        form = UserLoginForm({'username': 'username'})
        self.assertEqual(form.errors['password'], ['This field is required.'])

    def test_login(self):
        form = UserLoginForm({'username': 'username','password': 'password'})
        self.assertTrue(form.is_valid())

    def test_registration_passwords_check_err(self):
        form = UserRegistrationForm({'username': 'admin','email': 'admin@example.com','password1': 'password1','password2': 'password2'})
        self.assertEqual(form.errors['password2'], ['Passwords must match'])
        form = UserRegistrationForm({'username': 'admin','email': 'admin@example.com','password1': 'password1','password2': ''})
        self.assertEqual(form.errors['password2'], ['This field is required.'])

    def test_registration_email_to_be_unique(self):
        User.objects.create_user(username='username2',email='username2@testit.com')
        form = UserRegistrationForm({'username': 'username3','email': 'username2@testit.com','password1': 'password1','password2': 'password2'})
        self.assertEqual(form.errors['email'], ['Email address must be unique'])
                   
    def test_filter_view(self):
        form = FilterView({'group_by': 'player'})
        self.assertTrue(form.is_valid())
        self.assertIn('<option value="player" selected>PLAYERS</option>', str(form))