from django.shortcuts import render
from influence.models import Influence
from django.db.models import Count
import json

# Create your views here.
def show_graph(request):
    #i.upvotes.filter(influences=i.pk) # Choices are: id, influences, users_vote, vote_levels
    #i.vote_levels.filter(influence_id=i.pk, level=1) Choices are: id, influence, influence_id, level, users_vote, users_vote_id
    
    ''' we retrieve number of views and each category that has been upvoted for that influence, its strength doubles, thus we multiply by two ''' 
    influences = [{'Category': 'Influence', 'viewsUpv': int(i.views) + int((i.vote_levels.filter(influence_id=i.pk, level=1).count()) * 2), 'Status': i.status} for i in Influence.objects.filter(views__gt=0)]

    #influences1 = [{'Category': 'Influence', 'viewsUpv': int(i.views) + int((i.vote_levels.filter(influence_id=i.pk, level=1).count()) * 2), 'Status': i.status} for i in Influence.objects.filter(views__gt=0)]
    
    ''' convert to json string '''
    jsonData = json.dumps(influences)
    #jsonData = json.dumps(list(influences + influences1))
    
    args = {"jsonData": jsonData}
    return render(request, 'graphs.html', args)