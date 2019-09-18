from django.shortcuts import render
from influence.models import Influence
from creativity.models import Creativity
from threat.models import Threat
from django.db.models import Count
import json

def show_graph(request):
    """ Three cross-filter graphs views counter implementation 
    We retrieve number of views per category [Influence, Creativity, Threat]. 
    If a card has been upvoted, its strength doubles, thus that upvoted view counts for two 
    """
    influences = [{'Category': 'Influence', 'viewsUpv': int(i.views) + int((i.vote_levels.filter(influence_id=i.pk, level=1).count()) * 2), 'Status': i.status.capitalize()} for i in Influence.objects.filter(views__gt=0)]
    creativities = [{'Category': 'Creativity', 'viewsUpv': int(c.views) + int((c.creati_vote_levels.filter(creativity_id=c.pk, level=1).count()) * 2), 'Status': c.status.capitalize()} for c in Creativity.objects.filter(views__gt=0)]
    threats = [{'Category': 'Threat', 'viewsUpv': int(t.views) + int((t.threat_vote_levels.filter(threat_id=t.pk, level=1).count()) * 2), 'Status': t.status.capitalize()} for t in Threat.objects.filter(views__gt=0)]

    # convert to json string
    jsonData = json.dumps(list(influences + creativities + threats))
    
    # add json string as a parameter which will then insert it on the js script to apply D3 DC js
    args = {"jsonData": jsonData}
    return render(request, 'graphs.html', args)