from django.shortcuts import render

# Create your views here.
def all_influences(request):
    """Return the all_influences.html file"""
    return render(request, 'all_influences.html')
    
    
def add_influence(request):
    """Return the add_influence.html file"""
    return render(request, 'add_influence.html')    