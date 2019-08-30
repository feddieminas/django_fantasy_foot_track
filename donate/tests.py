from django.test import TestCase
from django.contrib.auth.models import User
from .models import Donate

''' Donate '''

class Tests(TestCase):
    
    def test_page_html_and_model(self):
        User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        
        # page_html
        page = self.client.get("/donate/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "donate.html")
        
        # Check model
        donate = Donate(user=User.objects.get(username='username'), donation=0.5)
        donate.save()         
        
        self.assertEqual(donate.user, User.objects.get(username='username'))
        self.assertEqual(donate.donation, 0.5)
        
        # Delete Objects
        user = User.objects.get(username='username')
        donate = Donate.objects.get(user=user)
        donate.delete()        
        user.delete()