from django import forms
from .models import Influence, Comment

class CreateInfluenceForm(forms.ModelForm):
    class Meta:
        model = Influence
        fields = ('motive', 'name', 'desc', 'status')
        labels = {
            'desc': 'Description',
        }        
        
class CreateInfluenceCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)  
        labels = {
            'content': 'Comment',
        }