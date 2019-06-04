from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Influence(models.Model):
    MOTIVE_CHOICES = ( 
        ('player', 'Player'),
        ('feature', 'Feature'),
    )    
    
    STATUS_CHOICES = ( 
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    
    owner = models.ForeignKey(User, related_name='influences', on_delete=models.SET_NULL, null=True)
    motive = models.CharField(max_length=7, choices=MOTIVE_CHOICES, default="player")
    name = models.CharField(max_length=75)
    desc = models.TextField(max_length=500)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default="low")
    views = models.IntegerField(default=0)
    upvotes = models.ManyToManyField('UpVote', through='Likeability', related_name='influences')
    created_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name    


class Comment(models.Model):
    influence = models.ForeignKey(Influence, related_name='comments', on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=500)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    
    def __str__(self):
        return self.content    
        

class UpVote(models.Model):
    users_vote = models.IntegerField(unique=True, null=True) 
    
    def __str__(self):
        return str(self.users_vote)

class Likeability(models.Model): # Through Model
    NOVOTE = 0
    UPVOTE = 1
    VOTE_CHOICES = (
        (NOVOTE, 'NOVOTE'),
        (UPVOTE, 'UPVOTE'),
    )

    influence = models.ForeignKey(Influence, related_name='vote_levels', on_delete=models.CASCADE, null=True)
    users_vote = models.ForeignKey(UpVote, related_name='vote_levels', on_delete=models.SET_NULL, blank=True, null=True)
    level = models.IntegerField(choices=VOTE_CHOICES, default=NOVOTE)
    
    class Meta:
        unique_together = ('influence', 'users_vote',)    
        
    def __str__(self):
        return "{0} - User_Vote {1} - Vote {2}".format(self.influence, self.users_vote, self.level)        