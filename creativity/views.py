from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Creativity, Comment, UpVote, Likeability
from .forms import CreateCreativityForm, CreateCreativityCommentForm
from django.db.models import Q, F
from functools import reduce
import operator
from django.utils import timezone
import datetime


def cre_save_curr_page(request):
    """ save current page value from prev next pagination in all_creativities.html, 
    to achieve rendering the last page seen after viewing a card from that page 
    """
    cre_curr_page = request.GET.get('cre_curr_page', None)
    request.session['cre_curr_page'] = 1 if cre_curr_page is None else int(cre_curr_page)   
    data = {
        'got_saved': bool(cre_curr_page)
    }
    return JsonResponse(data)


def all_creativities(request):
    """ Return the all_creativities.html file
    """
    
    # Search Button query category queryset values
    filterquery = False
    query = request.GET.get('q')
    if query:
        query_list = query.split()
        creativities = Creativity.objects.filter(
            reduce(operator.and_, (Q(motive__icontains=q[0:4]) for q in query_list)) |
            reduce(operator.and_, (Q(name__icontains=q) for q in query_list)) |
            reduce(operator.and_, (Q(desc__icontains=q) for q in query_list))
        ).order_by("-created_date")
        filterquery = creativities.exists()
    else:
        creativities = Creativity.objects.all().order_by("-created_date")
    
    # Number of Upvotes and Days category has been created
    creUpvotesAndDays = {}
    for cre in creativities:
        creUpvotesAndDays[str(cre.id)] = {}
        
        upvotes = cre.creati_vote_levels.filter(level=1).count()
        creUpvotesAndDays[str(cre.id)]['upvotes'] = upvotes
        
        daysdiff = abs(timezone.now().date() - cre.created_date.date()).days
        if daysdiff >= 365:
            yearsCount = int(daysdiff/365)
            creUpvotesAndDays[str(cre.id)]['daysyear'] = str(yearsCount) + " years ago" if yearsCount > 1 else "1 year ago"
        else:
            daysEval = lambda d: 'Today' if d == 0 else ('1 day ago' if d == 1 else str(d) + " days ago")
            creUpvotesAndDays[str(cre.id)]['daysyear'] = daysEval(daysdiff)
    
    # init a session variable list for a view list, for a same session same user not count a viewed category more than one time
    if 'viewlist' not in request.session:
        request.session['viewlist']=[]
    
    # init a session variable for current page  
    if 'cre_curr_page' not in request.session:    
        request.session['cre_curr_page']=1
    
    # status three [low, medium, high] background and font color that will be filtered with registered filters on template tags
    colorsIndex = {"high": ["#2C3E50","white"], "medium": ["#95a5a6","black"], "low": ["#18BC9C", "black"]}
    
    args = {'creativities': creativities, 'creUpvotesAndDays': creUpvotesAndDays, 'colorsIndex':colorsIndex, 'filterquery': filterquery, 'cre_curr_page_views_py': request.session['cre_curr_page']}
    return render(request, 'all_creativities.html', args)
    
@login_required
def add_creativity(request, pk=None):
    """ Return the add_creativity.html file. Currently pk will always be none as it is considered an add category. 
    If pk would not be none, it is an edit category 
    """
    creativity = get_object_or_404(Creativity, pk=pk) if pk else None
    
    # create a category card [pk, owner, motive, name, desc, status, created_date ]
    if request.method == "POST":
        form = CreateCreativityForm(request.POST, instance=creativity)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()
            return redirect(view_creativity, form.pk)
    else:
        form = CreateCreativityForm(instance=creativity) 
        
    args = {'form':form}    
    return render(request, 'add_creativity.html', args)

@login_required    
def view_creativity(request, pk, view=''):
    """ Return the view_creativity.html file. Pk is the category created through the add_category view. 
    """
    
    # Retrieve category card or submit a not found page
    try:
        creativity = Creativity.objects.get(pk=pk)
    except Creativity.DoesNotExist:
        return HttpResponseNotFound("Page Not Found")
    
    # create a category card comment [pk, creativity, owner, content, created_date ]
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        form = CreateCreativityCommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.creativity = creativity
            form.save()
        return redirect(view_creativity, creativity.pk)
    else:
        form = CreateCreativityCommentForm(instance=creativity)     
    
        # Auto-increment number of views when a user enters into a category card one time for current session 
        if view == "view" or creativity.views==0:
            viewlist = request.session['viewlist']
            if not (str(request.user.id) + "c" + str(pk)) in viewlist:
                creativity.views = F('views') + 1
                creativity.save()
                viewlist.append(str(request.user.id) + "c" + str(pk))
                request.session['viewlist'] = viewlist
        
        # Comments filter existing 
        comments = Comment.objects.filter(creativity__pk=creativity.pk)
    
        # UpVotes model. Create candidate user (or get if has already been created previously) for future potential upvote. 
        # Candidate user is the user of the page 
        users_vote, created = UpVote.objects.get_or_create(users_vote=request.user.id,)
        
        # Likeability filter existing
        likeability = Likeability.objects.filter(creativity=creativity)
        
        # If user_vote has been created previously and likeability model already exists for this category card, 
        # check if a user has actually viewed the current category card
        check_users_vote_has_val = False
        if not created and likeability.exists():
            check_users_vote_has_val = users_vote.creativities.filter(name=creativity.name, created_date=creativity.created_date)
        
        # If at least one of the options that user_vote has been created now or likeability model already exists for this category card, 
        # or a user first time views the current category card, then create a Likeability model 
        if any([created, not likeability.exists(), not check_users_vote_has_val]): 
            userlikeNoVote = Likeability(creativity=creativity, users_vote=users_vote, level=0,)
            userlikeNoVote.save()
        
        # Calculate number of existing upvotes and tell whether a user has upvoted already this category card, to prevent duplication
        userlikeUpVotes = 0
        user_has_upvote = False
        if likeability.exists():
            for l in likeability.iterator():
                if l.level == 1: # number of UpVotes
                    userlikeUpVotes += 1
                if l.users_vote == users_vote and l.level == 1: # if user has UpVoted this category
                    user_has_upvote = True
    
    args = {'creativity': creativity, "comments": comments, "upvotes_total": userlikeUpVotes, "user_has_upvote": user_has_upvote, 'form':form} 
    return render(request, 'view_creativity.html', args)

@login_required
def cre_user_upvote(request, pk):
    """ Returns no html file, it redirects to view_creativity.html. Pk is the category created through the add_category view 
    """
    
    # Via ManyToMany Relationship, we need to retrieve the category card and user to be able to assign 
    # the likeability level value to 1 (i.e. upvote)
    creativity = get_object_or_404(Creativity, pk=pk)
    likeit = get_object_or_404(Likeability, creativity=creativity, users_vote=UpVote.objects.get(users_vote=request.user.id,))
    likeit.level = 1
    likeit.save()
    return redirect(view_creativity, creativity.pk)
   
    
    
    
    
    
    
    
    
    
