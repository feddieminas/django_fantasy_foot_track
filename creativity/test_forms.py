from django.test import TestCase
from .forms import CreateCreativityForm, CreateCreativityCommentForm

""" Creativities Forms 
"""
class TestForm(TestCase):
    
    def test_creativity_with_required_values(self):
        form = CreateCreativityForm({'motive': 'player', 'name': "Test1", 'desc': "create a test1", 'status': "low"})
        self.assertTrue(form.is_valid())
        
    def test_creativity_less_or_empty_fields(self):
        form = CreateCreativityForm({'motive': 'player', 'name': ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [u'This field is required.'])

class TestCommentForm(TestCase):

    def test_creativity_comment_with_required_values(self):
        form = CreateCreativityCommentForm({'content': "i am a test comment"})
        self.assertTrue(form.is_valid())