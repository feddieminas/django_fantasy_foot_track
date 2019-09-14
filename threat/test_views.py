from django.test import TestCase
from .models import Threat, UpVote, Likeability
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import json

''' Threats Views '''

class TestViews(TestCase):
    """ Testid = [test_get_all_threats_page, test_add_threat_page, test_view_threat_views_count_user_has_viewed,
    test_view_threat_usersvote_likeability_and_upvote, test_add_threat_comment_page] """
    Testid = [0,0,0,0,0] # def tests
    
    def goto_delete_objects_or_continue_other_tests(self):
        TestidSum = sum(TestViews.Testid)
        if TestidSum == 5:
            self.delete_objects()
        self.client.logout()
        
    def the_Session_For_View_Cat(self):
        session = self.client.session 
        session['viewlist'] = []
        session.save()        
    
    def setUp(self):
        User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        threat = Threat(motive='player', name="Test2", desc="test2 description", status="high")
        threat.save() 
        users_vote, created = UpVote.objects.get_or_create(users_vote=User.objects.get(username='username').id,)
        userlikeNoVote = Likeability(threat=threat, users_vote=users_vote, level=0,)
        userlikeNoVote.save()
    
    def test_get_all_threats_page_and_save_curr_page_is_valid(self):
        ''' all_threats page '''
        page = self.client.get("/threats/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "all_threats.html")
        ''' save_curr_page response - test to see the view is functioning and returns a valid JSON response '''
        response = self.client.get('/threats/ajax/thr_save_curr_page/',content_type='application/json')
        self.assertEqual(json.loads(response.content.decode('utf-8')),{'got_saved': False})
        TestViews.Testid[0] = 1
        self.goto_delete_objects_or_continue_other_tests()
    
    def test_all_threats_template_tags(self):
        ''' threats not exist '''
        thr = Threat.objects.get(name="Test2")
        thr.delete()
        page = self.client.get("/threats/")
        self.assertNotContains(page, 'id="showAllThr" class="thr--bg-fontcolor w115"') 
        self.assertNotContains(page, 'style="color:white;background-color:#2C3E50;')        
        ''' threats exist '''
        threat = Threat(motive='player', name="Test2", desc="test2 high description", status="high")
        threat.save() 
        page = self.client.get("/threats/")
        self.assertContains(page, 'id="showAllThr" class="thr--bg-fontcolor w115"') 
        self.assertContains(page, 'style="color:white;background-color:#2C3E50;')
        TestViews.Testid[1] = 1
        self.goto_delete_objects_or_continue_other_tests()    
    
    def test_add_threat_page(self):
        page = self.client.get("/threats/add/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "add_threat.html")
        TestViews.Testid[2] = 1 
        self.goto_delete_objects_or_continue_other_tests()
    
    def test_view_threat_views_count_user_has_viewed(self):
        thr = Threat.objects.get(name="Test2")
        self.assertEqual(thr.views, 0)
        self.the_Session_For_View_Cat()
        self.client.get("/threats/{0}/view/".format(int(thr.pk)))
        thr = Threat.objects.get(name="Test2")
        self.assertEqual(thr.views, 1)
        TestViews.Testid[3] = 1 
        self.goto_delete_objects_or_continue_other_tests()
    
    def test_view_threat_usersvote_likeability_and_upvote(self):
        ''' view_threat '''
        thr = Threat.objects.get(name="Test2")
        self.the_Session_For_View_Cat()
        page = self.client.get("/threats/{0}/".format(int(thr.pk)))
        self.assertEqual(page.status_code, 200)
        likeability = Likeability.objects.filter(threat=thr)
        self.assertTrue(likeability.exists())
        user = User.objects.get(username='username')
        users_vote, created = UpVote.objects.get_or_create(users_vote=user.id,)
        self.assertFalse(created) # because already has been created when previously loaded the page
    
        ''' user_upvote '''
        page = self.client.get("/threats/{0}/thr_vote/".format(int(thr.pk)))
        self.assertRedirects(page,"/threats/{0}/".format(int(thr.pk)))
        likeit = get_object_or_404(Likeability, threat=thr, users_vote=UpVote.objects.get(users_vote=user.id,))
        self.assertEqual(likeit.level, 1)
        TestViews.Testid[4] = 1 
        self.goto_delete_objects_or_continue_other_tests()
    
    def delete_objects(self): # delete_objects
        try:
            user = User.objects.get(username='username')
            thr = Threat.objects.get(name="Test2")
            users_vote = UpVote.objects.get(users_vote=user.id,)
            thr.upvotes.through.objects.get(users_vote=users_vote).delete()   
            thr.delete() 
            users_vote.delete()
            user.delete()
        except:
            print("def test_delete_objects in test_views.py produces an ERROR")
        # print(Threat.objects.all(), UpVote.objects.all(), Likeability.objects.all()) # one can uncomment to see that queryset results to empty
        

    