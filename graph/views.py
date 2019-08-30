from django.shortcuts import render
from influence.models import Influence
from creativity.models import Creativity
from threat.models import Threat
from django.db.models import Count
import json

# Create your views here.
def show_graph(request):
    # remove 300
    
    ''' we retrieve number of views and each category that has been upvoted for that influence, its strength doubles, thus we multiply by two ''' 
    influences = [{'Category': 'Influence', 'viewsUpv': int(i.views) + int((i.vote_levels.filter(influence_id=i.pk, level=1).count()) * 2), 'Status': i.status.capitalize()} for i in Influence.objects.filter(views__gt=0)]
    creativities = [{'Category': 'Creativity', 'viewsUpv': int(c.views) + int((c.creati_vote_levels.filter(creativity_id=c.pk, level=1).count()) * 2), 'Status': c.status.capitalize()} for c in Creativity.objects.filter(views__gt=0)]
    threats = [{'Category': 'Threat', 'viewsUpv': int(t.views) + int((t.threat_vote_levels.filter(threat_id=t.pk, level=1).count()) * 2), 'Status': t.status.capitalize()} for t in Threat.objects.filter(views__gt=0)]

    ''' convert to json string '''
    jsonData = json.dumps(list(influences + creativities + threats))
    
    args = {"jsonData": jsonData}
    return render(request, 'graphs.html', args)