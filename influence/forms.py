from django import forms
from .models import Influence, Comment

''' add an influence '''
class CreateInfluenceForm(forms.ModelForm):
    class Meta:
        model = Influence
        fields = ('motive', 'name', 'desc', 'status')
        labels = {
            'desc': 'Description',
            'status': 'Status Importance',
        }        

''' add an influence comment '''        
class CreateInfluenceCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)  
        labels = {
            'content': 'Comment',
        }