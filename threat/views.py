from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Threat, Comment, UpVote, Likeability
from .forms import CreateThreatForm, CreateThreatCommentForm
from django.db.models import Q, F
from functools import reduce
import operator
from django.utils import timezone
import datetime

# Create your views here.
def thr_save_curr_page(request):
    """ save current page value from prev next pagination in all_threats.html, 
    to achieve rendering the last page seen after viewing a card from that page """
    
    thr_curr_page = request.GET.get('thr_curr_page', None)
    request.session['thr_curr_page'] = 1 if thr_curr_page is None else int(thr_curr_page)   
    data = {
        'got_saved': bool(thr_curr_page)
    }
    return JsonResponse(data)


def all_threats(request):
    """Return the all_threats.html file"""
    
    """ Search Button query category queryset values """
    filterquery = False
    query = request.GET.get('q')
    if query:
        query_list = query.split()
        threats = Threat.objects.filter(
            reduce(operator.and_, (Q(motive__icontains=q[0:4]) for q in query_list)) |
            reduce(operator.and_, (Q(name__icontains=q) for q in query_list)) |
            reduce(operator.and_, (Q(desc__icontains=q) for q in query_list))
        ).order_by("-created_date")
        filterquery = threats.exists()
    else:
        threats = Threat.objects.all().order_by("-created_date")
    
    """ Number of Upvotes and Days category has been created """
    thrUpvotesAndDays = {}
    for thr in threats:
        thrUpvotesAndDays[str(thr.id)] = {}
        
        upvotes = thr.threat_vote_levels.filter(level=1).count()
        thrUpvotesAndDays[str(thr.id)]['upvotes'] = upvotes
        
        daysdiff = abs(timezone.now().date() - thr.created_date.date()).days
        if daysdiff >= 365:
            yearsCount = int(daysdiff/365)
            thrUpvotesAndDays[str(thr.id)]['daysyear'] = str(yearsCount) + " years ago" if yearsCount > 1 else "1 year ago"
        else:
            daysEval = lambda d: 'Today' if d == 0 else ('1 day ago' if d == 1 else str(d) + " days ago")
            thrUpvotesAndDays[str(thr.id)]['daysyear'] = daysEval(daysdiff)
    
    """ init a session variable list for a view list, for a same session same user not count a viewed category more than one time """
    if 'viewlist' not in request.session:
        request.session['viewlist']=[]
    
    """ init a session variable for current page """    
    if 'thr_curr_page' not in request.session:    
        request.session['thr_curr_page']=1
    
    """ status three [low, medium, high] background and font color that will be filtered with registered filters on template tags """
    colorsIndex = {"high": ["#2C3E50","white"], "medium": ["#95a5a6","black"], "low": ["#18BC9C", "black"]}
    
    args = {'threats': threats, 'thrUpvotesAndDays': thrUpvotesAndDays, 'colorsIndex':colorsIndex, 'filterquery': filterquery, 'thr_curr_page_views_py': request.session['thr_curr_page']}
    return render(request, 'all_threats.html', args)
    
@login_required
def add_threat(request, pk=None):
    """ Return the add_threat.html file. Currently pk will always be none as it is considered an add category. 
    If pk would not be none, it is an edit category """
    
    threat = get_object_or_404(Threat, pk=pk) if pk else None
    
    """ create a category card [pk, owner, motive, name, desc, status, created_date ] """
    if request.method == "POST":
        form = CreateThreatForm(request.POST, instance=threat)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()
            return redirect(view_threat, form.pk)
    else:
        form = CreateThreatForm(instance=threat) 
        
    args = {'form':form}    
    return render(request, 'add_threat.html', args)

@login_required   
def view_threat(request, pk, view=''):
    """ Return the view_threat.html file. Pk is the category created through the add_category view. """
    
    """ Retrieve category card or submit a not found page """
    try:
        threat = Threat.objects.get(pk=pk)
    except Threat.DoesNotExist:
        return HttpResponseNotFound("Page Not Found")
    
    """ create a category card comment [pk, threat, owner, content, created_date ] """
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        form = CreateThreatCommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.threat = threat
            form.save()
        return redirect(view_threat, threat.pk)
    else:
        form = CreateThreatCommentForm(instance=threat)     
    
        """ Auto-increment number of views when a user enters into a category card one time for current session """
        if view == "view" or threat.views==0: 
            viewlist = request.session['viewlist']
            if not (str(request.user.id) + "t" + str(pk)) in viewlist:
                threat.views = F('views') + 1
                threat.save()
                viewlist.append(str(request.user.id) + "t" + str(pk))
                request.session['viewlist'] = viewlist
                #request.session.modified = True
        
        """ Comments filter existing """
        comments = Comment.objects.filter(threat__pk=threat.pk)
    
        """ UpVotes model. Create candidate user (or get if has already been created previously) for future potential upvote. 
        Candidate user is the user of the page """ 
        users_vote, created = UpVote.objects.get_or_create(users_vote=request.user.id,)
        
        """ Likeability filter existing """
        likeability = Likeability.objects.filter(threat=threat)
        
        """ If user_vote has been created previously and likeability model already exists for this category card, 
        check if a user has actually viewed the current category card """
        check_users_vote_has_val = False
        if not created and likeability.exists():
            check_users_vote_has_val = users_vote.threats.filter(name=threat.name, created_date=threat.created_date)
        
        """ If at least one of the options that user_vote has been created now or likeability model already exists for this category card, 
        or a user first time views the current category card, then create a Likeability model """    
        if any([created, not likeability.exists(), not check_users_vote_has_val]): 
            userlikeNoVote = Likeability(threat=threat, users_vote=users_vote, level=0,)
            userlikeNoVote.save()
        
        """ Calculate number of existing upvotes and tell whether a user has upvoted already this category card, to prevent duplication """
        userlikeUpVotes = 0
        user_has_upvote = False
        if likeability.exists():
            for l in likeability.iterator():
                if l.level == 1: # number of UpVotes
                    userlikeUpVotes += 1
                if l.users_vote == users_vote and l.level == 1: # if user has UpVoted this category
                    user_has_upvote = True
    
    args = {'threat': threat, "comments": comments, "upvotes_total": userlikeUpVotes, "user_has_upvote": user_has_upvote, 'form':form} 
    return render(request, 'view_threat.html', args)

@login_required
def thr_user_upvote(request, pk):
    """ Returns no html file, it redirects to view_threat.html. Pk is the category created through the add_category view """
    
    """ Via ManyToMany Relationship, we need to retrieve the category card and user to be able to assign 
    the likeability level value to 1 (i.e. upvote) """
    threat = get_object_or_404(Threat, pk=pk)
    likeit = get_object_or_404(Likeability, threat=threat, users_vote=UpVote.objects.get(users_vote=request.user.id,))
    likeit.level = 1
    likeit.save()
    return redirect(view_threat, threat.pk)
   
    
    
    
    
    
    
    
    
    
