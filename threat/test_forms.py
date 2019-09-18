from django.test import TestCase
from .forms import CreateThreatForm, CreateThreatCommentForm

""" Threats Forms 
"""
class TestForm(TestCase):
    
    def test_threat_with_required_values(self):
        form = CreateThreatForm({'motive': 'player', 'name': "Test1", 'desc': "create a test1", 'status': "low"})
        self.assertTrue(form.is_valid())
        
    def test_threat_less_or_empty_fields(self):
        form = CreateThreatForm({'motive': 'player', 'name': ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [u'This field is required.'])

class TestCommentForm(TestCase):

    def test_threat_comment_with_required_values(self):
        form = CreateThreatCommentForm({'content': "i am a test comment"})
        self.assertTrue(form.is_valid())
