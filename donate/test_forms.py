from django.test import TestCase
from .forms import DonationForm, DonationModelForm

""" Donate Forms 
"""
class TestForm(TestCase):
    
    def test_donate_form(self):
        form = DonationForm({'credit_card_number': '', 'cvv': ''})
        self.assertFalse(form.is_valid())
        
    def test_donate_modelform(self):    
        form = DonationModelForm({'donation': 5.55})
        self.assertTrue(form.is_valid())