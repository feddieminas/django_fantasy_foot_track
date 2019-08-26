from django.test import TestCase
from .models import Creativity, UpVote, Likeability
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

''' Creativities Views '''

class TestViews(TestCase):
    """ Testid = [test_get_all_creativities_page, test_add_creativity_page, test_view_creativity_views_count_user_has_viewed,
    test_view_creativity_usersvote_likeability_and_upvote, test_add_creativity_comment_page] """
    Testid = [0,0,0,0] # def tests
    
    def goto_delete_objects_or_continue_other_tests(self):
        TestidSum = sum(TestViews.Testid)
        if TestidSum == 4:
            self.delete_objects()
        self.client.logout()        
    
    def setUp(self):
        User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        creativity = Creativity(motive='player', name="Test2", desc="test2 description", status="high")
        creativity.save() 
        users_vote, created = UpVote.objects.get_or_create(users_vote=User.objects.get(username='username').id,)
        userlikeNoVote = Likeability(creativity=creativity, users_vote=users_vote, level=0,)
        userlikeNoVote.save()
    
    def test_get_all_creativities_page_and_save_curr_page_is_valid(self):
        ''' all_creativities page '''
        page = self.client.get("/creativities/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "all_creativities.html")
        ''' save_curr_page response - test to see the view is functioning and returns a valid JSON response '''
        response = self.client.get('/creativities/ajax/save_curr_page/',content_type='application/json')
        self.assertJSONEqual(response.content,{'got_saved': False})
        TestViews.Testid[0] = 1
        self.goto_delete_objects_or_continue_other_tests()
    
    def test_add_creativity_page(self):
        page = self.client.get("/creativities/add/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "add_creativity.html")
        TestViews.Testid[1] = 1 
        self.goto_delete_objects_or_continue_other_tests()
    
    def test_view_creativity_views_count_user_has_viewed(self):
        cre = Creativity.objects.get(name="Test2")
        self.assertEqual(cre.views, 0)
        session = self.client.session 
        session['viewlist'] = []
        session.save()
        self.client.get("/creativities/{0}/view/".format(int(cre.pk)))
        cre = Creativity.objects.get(name="Test2")
        self.assertEqual(cre.views, 1)
        TestViews.Testid[2] = 1 
        self.goto_delete_objects_or_continue_other_tests()
    
    def test_view_creativity_usersvote_likeability_and_upvote(self):
        ''' view_creativity '''
        cre = Creativity.objects.get(name="Test2")
        page = self.client.get("/creativities/{0}/".format(int(cre.pk)))
        self.assertEqual(page.status_code, 200)
        likeability = Likeability.objects.filter(creativity=cre)
        self.assertTrue(likeability.exists())
        user = User.objects.get(username='username')
        users_vote, created = UpVote.objects.get_or_create(users_vote=user.id,)
        self.assertFalse(created) # because already has been created when previously loaded the page
    
        ''' user_upvote '''
        page = self.client.get("/creativities/{0}/cre_vote/".format(int(cre.pk)))
        self.assertRedirects(page,"/creativities/{0}/".format(int(cre.pk)))
        likeit = get_object_or_404(Likeability, creativity=cre, users_vote=UpVote.objects.get(users_vote=user.id,))
        self.assertEqual(likeit.level, 1)
        TestViews.Testid[3] = 1 
        self.goto_delete_objects_or_continue_other_tests()
    
    def delete_objects(self): # delete_objects
        try:
            user = User.objects.get(username='username')
            cre = Creativity.objects.get(name="Test2")
            users_vote = UpVote.objects.get(users_vote=user.id,)
            cre.upvotes.through.objects.get(users_vote=users_vote).delete()   
            cre.delete() 
            users_vote.delete()
            user.delete()
        except:
            print("def test_delete_objects in test_views.py produces an ERROR")
        # print(Creativity.objects.all(), UpVote.objects.all(), Likeability.objects.all()) # one can uncomment to see that queryset results to empty
        

    