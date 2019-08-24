from django import forms
from .models import Donate
import datetime

class DonationForm(forms.Form):
    
    MONTH_CHOICES = [(i, i) for i in range(1,13)]
    YEAR_CHOICES = [(i, i) for i in range(datetime.datetime.today().year, 2037)]
    
    credit_card_number = forms.CharField(label='Credit Card Number', required=False)
    cvv = forms.CharField(label='Security code (CVV)', required=False)
    expiry_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)
    
class DonationModelForm(forms.ModelForm):
    class Meta:
        model = Donate
        fields = ('donation',)
        labels = {
            'donation': 'Donation € - EUR',
        }        