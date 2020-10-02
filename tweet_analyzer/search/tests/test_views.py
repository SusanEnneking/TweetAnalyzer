
from django.test import TestCase
from common.view_test_mixin import ViewRequestFactoryTestMixin

from search.views import SearchTweets

class SearchViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    view_class = SearchTweets
    
    def test_get(self):
        self.is_callable()
