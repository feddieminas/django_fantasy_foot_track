from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseNotFound
from .models import Influence, Comment, UpVote, Likeability
from .forms import CreateInfluenceForm, CreateInfluenceCommentForm
from django.db.models import Q

# Create your views here.
def all_influences(request):
    """Return the all_influences.html file"""
    print("all_influence user_id", request.user.id)
    influences = Influence.objects.all()
    print("all_influences influences", influences)
    
    args = {'influences': influences}
    return render(request, 'all_influences.html', args)
    

def view_influence(request, pk, view=''):
    "Views on Influence Class, Upvote user_votes to add userid if needed and update, Likeability level add"
    try:
        influence = Influence.objects.get(pk=pk)
    except Influence.DoesNotExist:
        return HttpResponseNotFound("Page Not Found")
    
    # Influence
    if view == "view":
        influence.views += 1
        influence.save()
    
    # Comments
    comments = Comment.objects.filter(influence__pk=influence.pk)

    # UpVotes 
    users_vote, created = UpVote.objects.get_or_create(users_vote=request.user.id,)
    if not created:
        check_users_vote_has_val = users_vote.influences.filter(name=influence.name, created_date=influence.created_date)
    if any([created, not check_users_vote_has_val]): 
        userlikeNoVote = Likeability(influence=influence, users_vote=users_vote, level=0,)
        userlikeNoVote.save()
    
    likeability = Likeability.objects.filter(influence=influence)
    userlikeUpVotes = 0
    user_has_upvote = False
    if likeability.exists():
        for l in likeability.iterator():
            print(request.user.id, l.influence, l.users_vote, l.level)
            if l.level == 1: # number of UpVotes
                userlikeUpVotes += 1
            if l.users_vote == users_vote and l.level == 1: # if user has UpVoted this category
                user_has_upvote = True
    
    args = {'influence': influence, "comments": comments, "upvotes_total": userlikeUpVotes, "user_has_upvote": user_has_upvote} 
    return render(request, 'view_influence.html', args)
    
    
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


def user_upvote(request, pk):
    influence =  get_object_or_404(Influence, pk=pk)
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





# add_comment loop comments, then when finished view, go to all_infuences.html fix upvotes length and days     