from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseNotFound
from .models import Influence, Comment, UpVote, Likeability
from .forms import CreateInfluenceForm, CreateInfluenceCommentForm
from django.db.models import Q
from functools import reduce
import operator
from django.utils import timezone
import datetime

# fix all html+css files, first the view comment, then add roboto or similar - insert comments on all

# Create your views here.
def all_influences(request):
    """Return the all_influences.html file"""
    
    query = request.GET.get('q')
    if query:
        query_list = query.split()
        influences = Influence.objects.filter(
            reduce(operator.and_, (Q(name__icontains=q) for q in query_list)) |
            reduce(operator.and_, (Q(desc__icontains=q) for q in query_list))
        )
    else:
        influences = Influence.objects.all()
    
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
    
    if 'viewlist' not in request.session:
        request.session['viewlist']=[]
    
    colorsIndex = {"low": ["#2C3E50","white"], "medium": ["#95a5a6","black"], "high": ["#18BC9C", "black"]}
    
    args = {'influences': influences, 'infUpvotesAndDays': infUpvotesAndDays, 'colorsIndex':colorsIndex}
    return render(request, 'all_influences.html', args)
    

def add_influence(request, pk=None):
    """Return the add_influence.html file"""
    influence =  get_object_or_404(Influence, pk=pk) if pk else None
    
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
    "Views on Influence Class, Upvote user_votes to add userid if needed and update, Likeability level add"
    try:
        influence = Influence.objects.get(pk=pk)
    except Influence.DoesNotExist:
        return HttpResponseNotFound("Page Not Found")
    
    # Influence
    if view == "view":
        viewlist = request.session['viewlist']
        if not (str(request.user.id) + "i" + str(pk)) in viewlist:
            influence.views += 1
            influence.save()
            viewlist.append(str(request.user.id) + "i" + str(pk))
            request.session['viewlist'] = viewlist
            #request.session.modified = True
    
    # Comments
    comments = Comment.objects.filter(influence__pk=influence.pk)

    # UpVotes 
    users_vote, created = UpVote.objects.get_or_create(users_vote=request.user.id,)
    likeability = Likeability.objects.filter(influence=influence)
    
    check_users_vote_has_val = False
    if not created and likeability.exists():
        check_users_vote_has_val = users_vote.influences.filter(name=influence.name, created_date=influence.created_date)
    
    if any([created, not likeability.exists(), not check_users_vote_has_val]): 
        userlikeNoVote = Likeability(influence=influence, users_vote=users_vote, level=0,)
        userlikeNoVote.save()
    
    userlikeUpVotes = 0
    user_has_upvote = False
    if likeability.exists():
        for l in likeability.iterator():
            #print(request.user.id, l.influence, l.users_vote, l.level)
            if l.level == 1: # number of UpVotes
                userlikeUpVotes += 1
            if l.users_vote == users_vote and l.level == 1: # if user has UpVoted this category
                user_has_upvote = True
    
    args = {'influence': influence, "comments": comments, "upvotes_total": userlikeUpVotes, "user_has_upvote": user_has_upvote} 
    return render(request, 'view_influence.html', args)


def user_upvote(request, pk):
    influence = get_object_or_404(Influence, pk=pk)
    print(UpVote.objects.get(users_vote=request.user.id,))
    likeit = get_object_or_404(Likeability, influence=influence, users_vote=UpVote.objects.get(users_vote=request.user.id,))
    likeit.level = 1
    likeit.save()
    return redirect(view_influence, influence.pk)


def add_influ_comment(request, pk):
    """Return the add_influ_comment.html file"""
    influence =  get_object_or_404(Influence, pk=pk)
    
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