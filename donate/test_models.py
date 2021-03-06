""" Donate Test Models
"""

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Donate

class TestModels(TestCase):
    
    def test__model(self):
        User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        
        donate = Donate(user=User.objects.get(username='username'), donation=0.5)
        donate.save()         
        
        self.assertEqual(donate.user, User.objects.get(username='username'))
        self.assertEqual(donate.donation, 0.5)
        
        # Delete Objects
        user = User.objects.get(username='username')
        donate = Donate.objects.get(user=user)
        donate.delete()        
        user.delete()