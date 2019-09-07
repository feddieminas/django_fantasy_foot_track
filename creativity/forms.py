from django import forms
from .models import Creativity, Comment

''' add an creativity '''
class CreateCreativityForm(forms.ModelForm):
    class Meta:
        model = Creativity
        fields = ('motive', 'name', 'desc', 'status')
        labels = {
            'desc': 'Description',
            'status': 'Status Importance',
        }        
        widgets = {
          'desc': forms.Textarea(attrs={'rows':7, 'cols':25}),
        }              

''' add an creativity comment '''        
class CreateCreativityCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)  
        labels = {
            'content': '',
        }
        widgets = {
          'content': forms.Textarea(attrs={'rows':5, 'cols':25}),
        }