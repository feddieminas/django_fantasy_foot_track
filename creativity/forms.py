from django import forms
from .models import Creativity, Comment

class CreateCreativityForm(forms.ModelForm):
    """ add a creativity 
    """
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

      
class CreateCreativityCommentForm(forms.ModelForm):
    """ add a creativity comment 
    """  
    class Meta:
        model = Comment
        fields = ('content',)  
        labels = {
            'content': '',
        }
        widgets = {
          'content': forms.Textarea(attrs={'rows':5, 'cols':25}),
        }