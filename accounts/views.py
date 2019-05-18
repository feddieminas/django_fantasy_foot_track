from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required # stop people who aren't logged in for accessing this page, redirect to login page
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm
from django.template.context_processors import csrf


def index(request):
    """Return the index.html file"""
    # print("the print one", request.GET.get('category'))
    return render(request, 'index.html')

    
@login_required
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "You have succesfully been logged out")
    return redirect(reverse('index')) # reverse allows us to pass the name of url instead of the view (urls.py name="index")
    
    
def login(request):
    """Return a login page"""
    if request.user.is_authenticated: # we do not want to display the login page to users that are logged in it
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        
        if login_form.is_valid():
            user = auth.authenticate(username = request.POST['username'],
                                     password = request.POST['password'])
            
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have succesfully logged in!")
                
                if request.GET and request.GET['next'] !='':
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                else:
                    return redirect(reverse('index'))
                
            else:
                login_form.add_error(None, "Your username or password is incorrect")
        
    else:
        login_form = UserLoginForm()
        
    args = {"login_form": login_form, 'next': request.GET.get('next', '')}    
    return render(request, 'login.html', args)
    

def registration(request):
    """Render the registration page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST) # pass the values from request.POST
    
        if registration_form.is_valid(): # user == user.registration_form.save
            registration_form.save() #because we specify the model in meta class we do not need to specify model again here
    
        user = auth.authenticate(username=request.POST['username'],
                                 password=request.POST['password1'])
    
        if user:
            auth.login(user=user, request=request)
            messages.success(request, "You have succesfully registered")
            
            if request.GET and request.GET['next'] !='':
                next = request.GET['next']
                return HttpResponseRedirect(next)
            else:
                return redirect(reverse('profile'))   
        else:
            messages.error(request, "Unable to register your account at this time")
    
    else:
        registration_form = UserRegistrationForm()
        
    return render(request, 'registration.html', {
        "registration_form": registration_form})
        
@login_required        
def user_profile(request):
    """The user's profile page"""
    user = User.objects.get(email=request.user.email)
    return render(request, 'profile.html', {"profile": user})
    
    


        