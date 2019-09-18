from django import forms
from .models import Threat, Comment

""" add a threat 
"""
class CreateThreatForm(forms.ModelForm):
    class Meta:
        model = Threat
        fields = ('motive', 'name', 'desc', 'status')
        labels = {
            'desc': 'Description',
            'status': 'Status Importance',
        }        
        widgets = {
          'desc': forms.Textarea(attrs={'rows':7, 'cols':25}),
        }        

""" add a threat comment 
"""        
class CreateThreatCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)  
        labels = {
            'content': '',
        }
        widgets = {
          'content': forms.Textarea(attrs={'rows':5, 'cols':25}),
        }