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
        widget=forms.PasswordInput) #field is specified as property unless you change label
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput)
        
    class Meta: # meta classes used to determine things about the class itself, to specify model want to store info, want it to use to specify fields we are going to use
        model = User
        fields = ['username','email','password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email') # allows us to clean the email field and return the email once we're done
                                               # it's the cleaned_data we would use when use is_valid method     
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username): # filter in db if existing email exists
            raise forms.ValidationError(u'Email address must be unique')
        return email
        
    def clean_password2(self): # same with clean email you do on password
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if not password1 or not password2:
            raise ValidationError("Please confirm your password")
            
        if password1 != password2:
            raise ValidationError("Passwords must match")
            
        return password2
        
        