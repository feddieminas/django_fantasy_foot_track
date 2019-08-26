from django.test import TestCase
from .models import Creativity, UpVote, Likeability
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction

''' Creativities Models '''

class TestModels(TestCase):
    u = User.objects.get(pk=1)
    creativity = None
    upvote = None
    likeability = None
    Testid = [0,0,0] # [ creativity, upvote, likeability ]

    def test_creativity(self):
        if TestModels.creativity is None:
            TestModels.creativity = Creativity(motive='player', name="Test2", desc="test2 description", status="high")
            TestModels.creativity.save()
            TestModels.Testid[0] = TestModels.creativity.id 
            self.assertEqual(TestModels.creativity.name, 'Test2')
            self.assertEqual(TestModels.creativity.desc, "test2 description")
    
    def test_upvote(self):
        if TestModels.upvote is None:
            TestModels.upvote, created = UpVote.objects.get_or_create(users_vote=TestModels.u.pk,)
            TestModels.upvote.save()
            TestModels.Testid[1] = TestModels.upvote.id
            self.assertEqual(TestModels.upvote.users_vote, 1)
    
    def test_likeability(self):    
        if TestModels.likeability is None:
            TestModels.likeability = Likeability(creativity=TestModels.creativity, users_vote=TestModels.upvote, level=0,)
            TestModels.likeability.save()
            TestModels.Testid[2] = TestModels.likeability.id
            self.assertEqual(TestModels.likeability.creativity.name, 'Test2')
            self.assertEqual(TestModels.likeability.users_vote.users_vote, TestModels.u.pk)
            self.assertEqual(TestModels.likeability.level, 0) 
            
            """ test meta_class of unique_together in likeability model """
            try: 
                with transaction.atomic():
                    Likeability.objects.create(creativity=TestModels.creativity, users_vote=TestModels.upvote, level=0,)
                self.fail('Duplicate question allowed.')
            except IntegrityError:
                pass # Duplicate question not allowed. Unique_together in Meta Class work
        
    def test_delete_the_item_not_appear_in_db(self):
        if TestModels.creativity is None:
            self.test_creativity() 
        try:
            cre = Creativity.objects.get(id=TestModels.Testid[0])
            cre.delete()
        except Creativity.DoesNotExist:
            cre = None  

        if TestModels.upvote is None:
            self.test_upvote()
        upv = UpVote.objects.get(id=TestModels.Testid[1])
        upv.delete()          
        
        if TestModels.likeability is None:
            self.test_likeability()
        lk = Likeability.objects.get(id=TestModels.Testid[2])
        lk.delete()
    
        # print(Creativity.objects.all(), UpVote.objects.all(), Likeability.objects.all()) # one can uncomment to see that queryset results to empty