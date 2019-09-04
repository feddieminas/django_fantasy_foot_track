from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import Donate

''' Donate Views '''

class TestViews(TestCase):
    
    def setUp(self):
        User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
    
    def test_page_html(self):
        page = self.client.get("/donate/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "donate.html")
        
    ''' from https://github.com/hschafer2017/PCSwimming :-) '''    
        
    def test_card_accepted(self):
        response = self.client.post('/donate', {
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '12',
            'expiry_year': '2020',
            }, follow=True)

        for message in get_messages(response.wsgi_request):
            self.assertNotEqual('Your card was declined!', messages)

        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "index.html")

    def test_card_not_accepted(self):
        response = self.client.post('/donate', {
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '1',
            'expiry_year': '2019',
            }, follow=True)

        for message in get_messages(response.wsgi_request):
            self.assertEqual('Your card\'s expiration month is invalid.', messages)

        page = self.client.get("/donate/")
        self.assertEqual(page.status_code, 200)