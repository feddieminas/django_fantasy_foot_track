from django.test import TestCase
from .models import Threat, UpVote, Likeability
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction

''' Threats Models '''

class TestModels(TestCase):
    threat = None
    upvote = None
    likeability = None
    Testid = [0,0,0] # [ threat, upvote, likeability ]

    def setUp(self):
        u = User.objects.create_user('username', 'username@example.com', 'password')

    def test_threat(self):
        if TestModels.threat is None:
            TestModels.threat = Threat(motive='player', name="Test2", desc="test2 description", status="high")
            TestModels.threat.save()
            TestModels.Testid[0] = TestModels.threat.id 
            self.assertEqual(TestModels.threat.name, 'Test2')
            self.assertEqual(TestModels.threat.desc, "test2 description")
    
    def test_upvote(self):
        if TestModels.upvote is None:
            user = User.objects.get(pk=1)
            TestModels.upvote, created = UpVote.objects.get_or_create(users_vote=user.pk,) 
            TestModels.upvote.save()
            TestModels.Testid[1] = TestModels.upvote.id
            self.assertEqual(TestModels.upvote.users_vote, user.pk)
    
    def test_likeability(self):    
        if TestModels.likeability is None:
            user = User.objects.get(pk=1)
            TestModels.likeability = Likeability(threat=TestModels.threat, users_vote=TestModels.upvote, level=0,)
            TestModels.likeability.save()
            TestModels.Testid[2] = TestModels.likeability.id
            self.assertEqual(TestModels.likeability.threat.name, 'Test2')
            self.assertEqual(TestModels.likeability.users_vote.users_vote, user.pk)
            self.assertEqual(TestModels.likeability.level, 0) 
            
            """ test meta_class of unique_together in likeability model """
            try: 
                with transaction.atomic():
                    Likeability.objects.create(threat=TestModels.threat, users_vote=TestModels.upvote, level=0,)
                self.fail('Duplicate question allowed.')
            except IntegrityError:
                pass # Duplicate question not allowed. Unique_together in Meta Class work
        
    def test_delete_the_item_not_appear_in_db(self):
        if TestModels.threat is None:
            self.test_threat() 
        try:
            thr = Threat.objects.get(id=TestModels.Testid[0])
            thr.delete()
        except Threat.DoesNotExist:
            thr = None  

        if TestModels.upvote is None:
            self.test_upvote()
        upv = UpVote.objects.get(id=TestModels.Testid[1])
        upv.delete()          
        
        if TestModels.likeability is None:
            self.test_likeability()
        lk = Likeability.objects.get(id=TestModels.Testid[2])
        lk.delete()
    
        # print(Threat.objects.all(), UpVote.objects.all(), Likeability.objects.all()) # one can uncomment to see that queryset results to empty