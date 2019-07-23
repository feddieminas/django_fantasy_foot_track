from django.test import TestCase
from .models import Influence, UpVote, Likeability
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

''' Influences Views '''

class TestViews(TestCase):
    """ Testid = [test_get_all_influences_page, test_add_influence_page, test_view_influence_views_count_user_has_viewed,
    test_view_influence_usersvote_likeability_and_upvote, test_add_influence_comment_page] """
    Testid = [0,0,0,0,0] # def tests
    
    def goto_delete_objects_or_continue_other_tests(self):
        TestidSum = sum(TestViews.Testid)
        if TestidSum == 5:
            self.delete_objects()
        self.client.logout()        
    
    def setUp(self):
        User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        influence = Influence(motive='player', name="Test2", desc="test2 description", status="high")
        influence.save() 
        users_vote, created = UpVote.objects.get_or_create(users_vote=User.objects.get(username='username').id,)
        userlikeNoVote = Likeability(influence=influence, users_vote=users_vote, level=0,)
        userlikeNoVote.save()
    
    def test_get_all_influences_page(self):
        page = self.client.get("/influences/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "all_influences.html")
        TestViews.Testid[0] = 1 
        self.goto_delete_objects_or_continue_other_tests()
    
    def test_add_influence_page(self):
        page = self.client.get("/influences/add/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "add_influence.html")
        TestViews.Testid[1] = 1 
        self.goto_delete_objects_or_continue_other_tests()
    
    def test_view_influence_views_count_user_has_viewed(self):
        inf = Influence.objects.get(name="Test2")
        self.assertEqual(inf.views, 0)
        session = self.client.session 
        session['viewlist'] = []
        session.save()
        self.client.get("/influences/{0}/view/".format(int(inf.pk)))
        inf = Influence.objects.get(name="Test2")
        self.assertEqual(inf.views, 1)
        TestViews.Testid[2] = 1 
        self.goto_delete_objects_or_continue_other_tests()
    
    def test_view_influence_usersvote_likeability_and_upvote(self):
        ''' view_influence '''
        inf = Influence.objects.get(name="Test2")
        page = self.client.get("/influences/{0}/".format(int(inf.pk)))
        self.assertEqual(page.status_code, 200)
        likeability = Likeability.objects.filter(influence=inf)
        self.assertTrue(likeability.exists())
        user = User.objects.get(username='username')
        users_vote, created = UpVote.objects.get_or_create(users_vote=user.id,)
        self.assertFalse(created) # because already has been created when previously loaded the page
    
        ''' user_upvote '''
        page = self.client.get("/influences/{0}/inf_vote/".format(int(inf.pk)))
        self.assertRedirects(page,"/influences/{0}/".format(int(inf.pk)))
        likeit = get_object_or_404(Likeability, influence=inf, users_vote=UpVote.objects.get(users_vote=user.id,))
        self.assertEqual(likeit.level, 1)
        TestViews.Testid[3] = 1 
        self.goto_delete_objects_or_continue_other_tests()
    
    def test_add_influence_comment_page(self):
        inf = Influence.objects.get(name="Test2")
        page = self.client.get("/influences/{0}/add_comment/".format(int(inf.pk)))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "add_influ_comment.html") 
        TestViews.Testid[4] = 1 
        self.goto_delete_objects_or_continue_other_tests()
    
    def delete_objects(self): # delete_objects
        try:
            user = User.objects.get(username='username')
            inf = Influence.objects.get(name="Test2")
            users_vote = UpVote.objects.get(users_vote=user.id,)
            inf.upvotes.through.objects.get(users_vote=users_vote).delete()   
            inf.delete() 
            users_vote.delete()
            user.delete()
        except:
            print("def test_delete_objects in test_views.py produces an ERROR")
        # print(Influence.objects.all(), UpVote.objects.all(), Likeability.objects.all()) # one can uncomment to see that queryset results to empty
        

    