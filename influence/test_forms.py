""" Influences Test Forms 
"""

from django.test import TestCase
from .forms import CreateInfluenceForm, CreateInfluenceCommentForm

class TestForm(TestCase):
    
    def test_influence_with_required_values(self):
        form = CreateInfluenceForm({'motive': 'player', 'name': "Test1", 'desc': "create a test1", 'status': "low"})
        self.assertTrue(form.is_valid())
        
    def test_influence_less_or_empty_fields(self):
        form = CreateInfluenceForm({'motive': 'player', 'name': ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [u'This field is required.'])

class TestCommentForm(TestCase):

    def test_influence_comment_with_required_values(self):
        form = CreateInfluenceCommentForm({'content': "i am a test comment"})
        self.assertTrue(form.is_valid())
        