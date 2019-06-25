from django.test import TestCase
from .models import Influence, UpVote, Likeability
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

''' Influences '''

class TestViews(TestCase):
    def setUp(self):
        User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        influence = Influence(motive='player', name="Test2", desc="test2 description", status="high")
        influence.save()  
    
    def test_get_all_influences_page(self):
        page = self.client.get("/influences/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "all_influences.html")
    
    def test_add_influence_page(self):
        page = self.client.get("/influences/add")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "add_influence.html") 
    
    def test_view_influence_views_count_user_has_viewed(self):
        inf = Influence.objects.get(name="Test2")
        self.assertEqual(inf.views, 0)
        session = self.client.session 
        session['viewlist'] = []
        session.save()
        self.client.get("/influences/{0}/view/".format(int(inf.pk)))
        inf = Influence.objects.get(name="Test2")
        self.assertEqual(inf.views, 1)
    
    def test_view_influence_usersvote_likeability_and_upvote(self):
        ''' view_influence '''
        inf = Influence.objects.get(name="Test2")
        page = self.client.get("/influences/{0}/".format(int(inf.pk)))
        self.assertEqual(page.status_code, 200)
        likeability = Likeability.objects.filter(influence=inf)
        self.assertTrue(likeability.exists())
        user = User.objects.get(username='username')
        users_vote, created = UpVote.objects.get_or_create(users_vote=user.id,)
        self.assertFalse(created) #because already has been created when previously loaded the page
    
        ''' user_upvote '''
        page = self.client.get("/influences/{0}/inf_vote/".format(int(inf.pk)))
        self.assertRedirects(page,"/influences/{0}/".format(int(inf.pk)))
        likeit = get_object_or_404(Likeability, influence=inf, users_vote=UpVote.objects.get(users_vote=user.id,))
        self.assertEqual(likeit.level, 1)
    
    def test_add_influence_comment_page(self):
        inf = Influence.objects.get(name="Test2")
        page = self.client.get("/influences/{0}/add_comment/".format(int(inf.pk)))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "add_influ_comment.html")  
    
    def test_delete_objects(self):
        try:
            user = User.objects.get(username='username')
            inf = Influence.objects.get(name="Test2")
            users_vote, created = UpVote.objects.get_or_create(users_vote=user.id,)
            lk, created = Likeability.objects.get_or_create(influence=inf, users_vote=users_vote)
            inf.upvotes.through.objects.get(users_vote=users_vote).delete()   
            inf.delete() 
            user.delete()
        except:
            print("def test_delete_objects in test_views.py produces an ERROR")
        

    