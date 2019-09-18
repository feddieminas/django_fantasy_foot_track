from django.test import TestCase
from django.urls import reverse
from creativity.models import Creativity
from django.contrib.auth.models import User

""" Accounts Views 
"""
class TestIndexPostCall(TestCase):
    def setUp(self):
        User.objects.create_user(username='username', email="username@example.com", password='password')
    
    
    def test_login_then_return_to_main_page(self):
        page = self.client.post("/accounts/login/", {'username': 'username','password': 'password'})
        self.assertEqual(page.status_code, 302)
        self.assertRedirects(page, '/') 
     
        
    def test_registration_then_return_to_profile_and_go_main_page_if_logged(self):
        # go_main_page_if_logged
        self.client.login(username='username', password='password')
        self.assertRedirects(self.client.get("/accounts/register/"), '/') 
        self.client.logout()
        
        # register
        page = self.client.post("/accounts/register/", {'username': 'username','email': 'username@example.com','password1': 'password','password2': 'password'})
        self.assertEqual(page.status_code, 302)
        self.assertRedirects(page, '/accounts/profile/')   
     
        
    def test_profile_add_a_creativity_to_reflect_there_its_values(self):
        self.client.login(username='username', password='password')
        
        # add a creativity card, by the redirects, we have a one creation and a one view, then we upvote it and we have also an upvote
        session = self.client.session 
        session['viewlist'] = []
        session.save()    
        page = self.client.post("/creativities/add/", {'motive': 'player', 'name': 'Test1', 'desc': 'create a test1', 'status': 'low'}, follow=True)
        self.assertEqual(page.status_code, 200)
        cre = Creativity.objects.get(name="Test1")
        page = self.client.get("/creativities/{0}/cre_vote/".format(int(cre.pk)), follow=True)
        self.assertEqual(page.status_code, 200)
        
        # profile page 
        page = self.client.get("/accounts/profile/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed("profile.html")
        self.assertEqual(len(page.context['figuresInf']), 3)
        self.assertIn(list(page.context['figuresInf'].keys())[0], ['created', 'views', 'upvotes'])
        self.assertEqual(list(page.context['figuresInf'].values()), [0, 0, 0])          
        self.assertEqual(len(page.context['figuresCr']), 3)
        self.assertIn(list(page.context['figuresCr'].keys())[1], ['created', 'views', 'upvotes'])
        self.assertEqual(list(page.context['figuresCr'].values()), [1, 1, 1])        
        self.assertEqual(len(page.context['figuresTh']), 3)
        self.assertIn(list(page.context['figuresTh'].keys())[2], ['created', 'views', 'upvotes'])
        self.assertEqual(list(page.context['figuresTh'].values()), [0, 0, 0])
    
    
    """ Login with a user and post data on the dropdown filter form, check whether filter value 
    posted is equal to the one that is currently selected 
    """
    def test_main_page_call_post_method_filterViewCatgry(self):
        post_data = {'group_by': 'all'}
        page = self.client.post(reverse('index'), post_data)
        FilterViewLst = page.context["widget"]['optgroups']
        option_select_true = False
        for i in range(len(FilterViewLst)):
            if FilterViewLst[i][1][0]['selected'] is True:
                option_select_true = FilterViewLst[i][1][0]['value']
                break
        self.assertEqual(page.status_code, 200)
        self.assertEqual(post_data['group_by'], option_select_true)
        self.assertTemplateUsed(page, "index.html")  
    
        
    def test_delete_objects(self):
        try:
            user = User.objects.get(username='username')
            user.delete()
        except:
            print("user delete error on accounts app tests")        