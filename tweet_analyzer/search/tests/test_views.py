
from django.test import TestCase
from common.view_test_mixin import ViewRequestFactoryTestMixin

from search.views import Search, SavedSearch

class SearchViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    view_class = Search
    
    def test_get(self):
        self.is_callable()

class SavedSearchViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    view_class = SavedSearch
    
    def test_get(self):
        self.is_callable()