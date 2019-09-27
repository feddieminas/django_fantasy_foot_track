""" Donate Test Views
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import Donate

class TestViews(TestCase):
    
    def setUp(self):
        User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
    
    def test_page_html(self):
        page = self.client.get("/donate/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "donate.html")
        
    def test_card_should_be_accepted(self):
        response = self.client.post('/donate/', {
            'donation': 1,
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '12',
            'expiry_year': '2022',
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)

        for message in get_messages(response.wsgi_request):
            self.assertNotEqual('Your card was declined!', message)

        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "index.html")
    
    def test_card_no_validation(self):
        response = self.client.post('/donate/', {
            'donation': 1,
            'credit_card_number': '4242424248585',
            'cvv': '234586',
            'expiry_month': '10',
            'expiry_year': '2020',
            }, follow=True)

        self.assertEqual(response.status_code, 200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(list(get_messages(response.wsgi_request))), 1)
        self.assertEqual(str(messages[0]), 'We were unable to take a payment with that card!')
        
        self.assertDictEqual(response.context["alertResult"], {'result': 'danger'})
                
        page = self.client.get("/donate/")
        self.assertEqual(page.status_code, 200)