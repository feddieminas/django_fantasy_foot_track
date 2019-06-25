from django.test import TestCase
from .models import Influence, UpVote, Likeability
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction

''' Influences '''

class TestModels(TestCase):
    u = User.objects.get(pk=1)
    influence = None
    upvote = None
    likeability = None
    Testid = [0,0,0]

    def test_influence(self):
        if TestModels.influence is None:
            TestModels.influence = Influence(motive='player', name="Test2", desc="test2 description", status="high")
            TestModels.influence.save()
            TestModels.Testid[0] = TestModels.influence.id
            self.assertEqual(TestModels.influence.name, 'Test2')
            self.assertEqual(TestModels.influence.desc, "test2 description")
    
    def test_upvote(self):
        if TestModels.upvote is None:
            TestModels.upvote, created = UpVote.objects.get_or_create(users_vote=TestModels.u.pk,)
            TestModels.upvote.save()
            TestModels.Testid[1] = TestModels.upvote.id
            self.assertEqual(TestModels.upvote.users_vote, 1)
    
    def test_likeability(self):    
        if TestModels.likeability is None:
            TestModels.likeability = Likeability(influence=TestModels.influence, users_vote=TestModels.upvote, level=0,)
            TestModels.likeability.save()
            TestModels.Testid[2] = TestModels.likeability.id
            self.assertEqual(TestModels.likeability.influence.name, 'Test2')
            self.assertEqual(TestModels.likeability.users_vote.users_vote, TestModels.u.pk)
            self.assertEqual(TestModels.likeability.level, 0) 
            
            try:
                with transaction.atomic():
                    Likeability.objects.create(influence=TestModels.influence, users_vote=TestModels.upvote, level=0,)
                self.fail('Duplicate question allowed.')
            except IntegrityError:
                pass #'Duplicate question not allowed. Unique_together in Meta Class work'
        
    def test_delete_the_item_not_appear_in_db(self):
        if TestModels.influence is None:
            self.test_influence()    
        inf = Influence.objects.get(id=TestModels.Testid[0])
        inf.delete()

        if TestModels.upvote is None:
            self.test_upvote()
        upv = UpVote.objects.get(id=TestModels.Testid[1])
        upv.delete()          
        
        if TestModels.likeability is None:
            self.test_likeability()
        lk = Likeability.objects.get(id=TestModels.Testid[2])
        lk.delete()
    