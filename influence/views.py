from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Influence, Comment, UpVote, Likeability
from .forms import CreateInfluenceForm, CreateInfluenceCommentForm
from django.db.models import Q
from functools import reduce
import operator
from django.utils import timezone
import datetime

# Create your views here.
def save_curr_page(request):
    """ save current page value from prev next pagination in all_influences.html, 
    to achieve rendering the last page seen after viewing a card from that page """
    
    inf_curr_page = request.GET.get('inf_curr_page', None)
    request.session['inf_curr_page'] = 1 if inf_curr_page is None else int(inf_curr_page)   
    data = {
        'got_saved': bool(inf_curr_page)
    }
    return JsonResponse(data)


def all_influences(request):
    """Return the all_influences.html file"""
    
    """ Search Button query category queryset values """
    filterquery = False
    query = request.GET.get('q')
    if query:
        query_list = query.split()
        influences = Influence.objects.filter(
            reduce(operator.and_, (Q(name__icontains=q) for q in query_list)) |
            reduce(operator.and_, (Q(desc__icontains=q) for q in query_list))
        )
        filterquery = influences.exists()
    else:
        influences = Influence.objects.all()
    
    """ Number of Upvotes and Days category has been created """
    infUpvotesAndDays = {}
    for inf in influences:
        infUpvotesAndDays[str(inf.id)] = {}
        
        upvotes = inf.vote_levels.filter(level=1).count()
        infUpvotesAndDays[str(inf.id)]['upvotes'] = upvotes
        
        daysdiff = abs(timezone.now().date() - inf.created_date.date()).days
        if daysdiff >= 365:
            yearsCount = int(daysdiff/365)
            infUpvotesAndDays[str(inf.id)]['daysyear'] = str(yearsCount) + " years ago" if yearsCount > 1 else "1 year ago"
        else:
            daysEval = lambda d: 'Today' if d == 0 else ('1 day ago' if d == 1 else str(d) + " days ago")
            infUpvotesAndDays[str(inf.id)]['daysyear'] = daysEval(daysdiff)
    
    """ init a session variable list for a view list, for a same session same user not count a viewed category more than one time """
    if 'viewlist' not in request.session:
        request.session['viewlist']=[]
    
    """ init a session variable for current page """    
    if 'inf_curr_page' not in request.session:    
        request.session['inf_curr_page']=1
    
    """ status three [low, medium, high] background and font color that will be filtered with registered filters on template tags """
    colorsIndex = {"high": ["#2C3E50","white"], "medium": ["#95a5a6","black"], "low": ["#18BC9C", "black"]}
    
    args = {'influences': influences, 'infUpvotesAndDays': infUpvotesAndDays, 'colorsIndex':colorsIndex, 'filterquery': filterquery, 'inf_curr_page_views_py': request.session['inf_curr_page']}
    return render(request, 'all_influences.html', args)
    
@login_required
def add_influence(request, pk=None):
    """ Return the add_influence.html file. Currently pk will always be none as it is considered an add category. 
    If pk would not be none, it is an edit category """
    
    influence = get_object_or_404(Influence, pk=pk) if pk else None
    
    """ create a category card [pk, owner, motive, name, desc, status, created_date ] """
    if request.method == "POST":
        form = CreateInfluenceForm(request.POST, instance=influence)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()
            return redirect(view_influence, form.pk)
    else:
        form = CreateInfluenceForm(instance=influence) 
        
    args = {'form':form}    
    return render(request, 'add_influence.html', args)

    
def view_influence(request, pk, view=''):
    """ Return the view_influence.html file. Pk is the category created through the add_category view. """
    
    """ Retrieve category card or submit a not found page """
    try:
        influence = Influence.objects.get(pk=pk)
    except Influence.DoesNotExist:
        return HttpResponseNotFound("Page Not Found")
    
    
    """ Auto-increment number of views when a user enters into a category card one time for current session """
    if view == "view":
        viewlist = request.session['viewlist']
        if not (str(request.user.id) + "i" + str(pk)) in viewlist:
            influence.views += 1
            influence.save()
            viewlist.append(str(request.user.id) + "i" + str(pk))
            request.session['viewlist'] = viewlist
            #request.session.modified = True
    
    """ Comments filter existing """
    comments = Comment.objects.filter(influence__pk=influence.pk)

    """ UpVotes model. Create candidate user (or get if has already been created previously) for future potential upvote. 
    Candidate user is the user of the page """ 
    users_vote, created = UpVote.objects.get_or_create(users_vote=request.user.id,)
    
    """ Likeability filter existing """
    likeability = Likeability.objects.filter(influence=influence)
    
    """ If user_vote has been created previously and likeability model already exists for this category card, 
    check if a user has actually viewed the current category card """
    check_users_vote_has_val = False
    if not created and likeability.exists():
        check_users_vote_has_val = users_vote.influences.filter(name=influence.name, created_date=influence.created_date)
    
    """ If at least one of the options that user_vote has been created now or likeability model already exists for this category card, 
    or a user first time views the current category card, then create a Likeability model """    
    if any([created, not likeability.exists(), not check_users_vote_has_val]): 
        userlikeNoVote = Likeability(influence=influence, users_vote=users_vote, level=0,)
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
    
    args = {'influence': influence, "comments": comments, "upvotes_total": userlikeUpVotes, "user_has_upvote": user_has_upvote} 
    return render(request, 'view_influence.html', args)

@login_required
def user_upvote(request, pk):
    """ Returns no html file, it redirects to view_influence.html. Pk is the category created through the add_category view """
    
    """ Via ManyToMany Relationship, we need to retrieve the category card and user to be able to assign 
    the likeability level value to 1 (i.e. upvote) """
    influence = get_object_or_404(Influence, pk=pk)
    likeit = get_object_or_404(Likeability, influence=influence, users_vote=UpVote.objects.get(users_vote=request.user.id,))
    likeit.level = 1
    likeit.save()
    return redirect(view_influence, influence.pk)

@login_required
def add_influ_comment(request, pk):
    """Return the add_influ_comment.html file. Pk is the category created through the add_category view. 
    Comments are foreign keys to the category"""
    
    influence =  get_object_or_404(Influence, pk=pk)
    
    """ create a category card comment [pk, influence, owner, content, created_date ] """
    if request.method == "POST":
        form = CreateInfluenceCommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.influence = influence
            form.save()
        return redirect(view_influence, influence.pk)
    else:
        form = CreateInfluenceCommentForm(instance=influence) 
        
    args = {'form':form, "name": influence.name}    
    return render(request, 'add_influ_comment.html', args)   
    
    
    
    
    
    
    
    
    
