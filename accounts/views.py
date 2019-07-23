from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm, FilterView
from influence.models import Influence
from django.db.models import Count
from django.template.context_processors import csrf

def index(request):
    """Return the index.html file. figures calcs all three [low, medium, high] status total counter"""
    if request.method == "POST":
        filterView = FilterView(request.POST)
        if filterView.is_valid() == True:
            filterViewCatgry = request.POST.get('group_by') # dropdown form filter value by motive, [Player, Feature, ALL]
            if filterViewCatgry == "all":
                figuresInf = Influence.objects.all().values('status').annotate(total=Count('status')).order_by('-total')
            else:
                figuresInf = Influence.objects.filter(motive=filterViewCatgry).values('status').annotate(total=Count('status')).order_by('-total')
            figuresCr = {}
            figuresTh = {}    
    else:
        filterView = FilterView() # dropdown form filter by motive
        figuresInf = Influence.objects.filter(motive="player").values('status').annotate(total=Count('status')).order_by('-total')
        figuresCr = {}
        figuresTh = {}
    
    args = {"filterView": filterView, "figuresInf": figuresInf, "figuresCr": figuresCr, "figuresTh": figuresTh}    
    return render(request, 'index.html', args)

    
@login_required
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "You have succesfully been logged out")
    return redirect(reverse('index'))
    
    
def login(request):
    """Return a login page"""
    if request.user.is_authenticated: # not display login page if not logged in
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
        registration_form = UserRegistrationForm(request.POST)
    
        if registration_form.is_valid(): 
            registration_form.save() 
    
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
    
    


        