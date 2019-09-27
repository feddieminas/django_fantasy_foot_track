""" Graphs Test
"""

from django.test import TestCase

class Tests(TestCase):
    
    def test_page_html(self):
        page = self.client.get("/graph/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "graphs.html")
