from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

''' Index.html '''

"""
Login with a user and post data on the dropdown filter form, 
check whether filter value posted is equal to the one that is currently selected
"""
class TestIndexPostCall(TestCase):
    def setUp(self):
        User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
    
    def test_call_post_method_filterViewCatgry(self):
        post_data = {
            'group_by': 'all'
        }
        page = self.client.post(reverse('index'), post_data)
        FilterViewLst = page.context['group_choices']
        for i in range(len(FilterViewLst)):
            if FilterViewLst[i]['selected'] is True:
                option_select_true = FilterViewLst[i]['value']
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
        