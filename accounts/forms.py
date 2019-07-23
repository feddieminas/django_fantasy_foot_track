from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):
    """Form to be used to log users in"""
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class UserRegistrationForm(UserCreationForm):
    """Forms to be used to log users in"""
    
    password1 = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput) 
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput)
        
    class Meta: 
        model = User
        fields = ['username','email','password1', 'password2']
        
    def clean_email(self): 
        ''' email called once the content is already valid and populated '''
        email = self.cleaned_data.get('email') 
                                                   
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username): # filter in db if existing email exists
            raise forms.ValidationError(u'Email address must be unique')
        return email
        
    def clean_password2(self):
        ''' password conf called once the content is already valid and populated '''
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if not password1 or not password2:
            raise ValidationError("Please confirm your password")
            
        if password1 != password2:
            raise ValidationError("Passwords must match")
            
        return password2
        
    
class FilterView(forms.Form): 
    """ dropdown form filter by motive """
    GROUP_BY_CHOICES = [
        ('player', 'PLAYERS'),
        ('feature', 'FEATURES'),
        ('all', 'ALL')
    ]
    group_by = forms.ChoiceField(choices=GROUP_BY_CHOICES, label='')        