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
        widgets = {
          'desc': forms.Textarea(attrs={'rows':7, 'cols':25}),
        }              

''' add an influence comment '''        
class CreateInfluenceCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)  
        labels = {
            'content': '',
        }
        widgets = {
          'content': forms.Textarea(attrs={'rows':5, 'cols':25}),
        }