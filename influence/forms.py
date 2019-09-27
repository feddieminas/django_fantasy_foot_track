from django import forms
from .models import Influence, Comment

class CreateInfluenceForm(forms.ModelForm):
    """ add an influence 
    """
    class Meta:
        model = Influence
        fields = ('motive', 'name', 'desc', 'status')
        labels = {
            'desc': 'Description',
            'status': 'Status Importance',
        }        
        widgets = {
          'desc': forms.Textarea(attrs={'rows':7, 'cols':25}),
        }              


class CreateInfluenceCommentForm(forms.ModelForm):
    """ add an influence comment 
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