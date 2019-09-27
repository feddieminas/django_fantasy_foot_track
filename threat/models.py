""" Category Threat

The main first class Threat has all its field attributes plus the owner that creates it 
(foreign key refer to the User Model). A User can create multiple cards (becomes an owner).
Second class called Comment is linked to the main first Class. Its category card can receive 
many comments and by different users (included the owner himself/herself).

Many to Many Relationship :
Main First Class Upvotes is linked to Class Upvote and Likeability. Class Upvote stores the
pk value of the users (from the User Model). Field upvote.users_vote is linked with the last class 
likeability.users_vote field. The other main field of the Likeability class is the threat 
(linked to the main first class), as a category card can receive any upvotes or not and from 
different users. 

No Likeability can have more than a same user voting to the same category card. 
A user can simply either not upvote (NOVOTE) or upvote (UPVOTE) to one card.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Threat(models.Model):
    """ Threat Card
    """    
    MOTIVE_CHOICES = ( 
        ('player', 'Player'),
        ('feature', 'Feature'),
    )    
    
    STATUS_CHOICES = ( 
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    
    owner = models.ForeignKey(User, related_name='threats', on_delete=models.SET_NULL, null=True)
    motive = models.CharField(max_length=7, choices=MOTIVE_CHOICES, default="player")
    name = models.CharField(max_length=75)
    desc = models.TextField(max_length=500)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default="low")
    views = models.IntegerField(default=0)
    upvotes = models.ManyToManyField('UpVote', through='Likeability', related_name='threats')
    created_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name    


class Comment(models.Model):
    """ Threat Card Comments
    """    
    threat = models.ForeignKey(Threat, related_name='threat_comments', on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, related_name='threat_comments', on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=500)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    
    def __str__(self):
        return self.content    
        

class UpVote(models.Model): 
    """ Stores userIDs [1,2,3,4,etc] for potential Upvoting or Not
    """
    users_vote = models.IntegerField(unique=True, null=True) 
    
    def __str__(self):
        return str(self.users_vote)

class Likeability(models.Model):
    """ Through Model
    """    
    NOVOTE = 0
    UPVOTE = 1
    VOTE_CHOICES = (
        (NOVOTE, 'NOVOTE'),
        (UPVOTE, 'UPVOTE'),
    )

    threat = models.ForeignKey(Threat, related_name='threat_vote_levels', on_delete=models.CASCADE, null=True)
    users_vote = models.ForeignKey(UpVote, related_name='threat_vote_levels', on_delete=models.SET_NULL, blank=True, null=True)
    level = models.IntegerField(choices=VOTE_CHOICES, default=NOVOTE)
    
    class Meta:
        unique_together = ('threat', 'users_vote',) # one row, one user enters / modifies choice to one category card      
        
    def __str__(self):
        return "{0} - User_Vote {1} - Vote {2}".format(self.threat, self.users_vote, self.level)        
