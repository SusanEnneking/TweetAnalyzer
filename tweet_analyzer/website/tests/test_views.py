from django.test import TestCase
from common.view_test_mixin import ViewRequestFactoryTestMixin

from website.views import Welcome, About


class WelcomeViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    view_class = Welcome

    def test_get(self):
        self.is_callable()


class AboutViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    view_class = About

    def test_get(self):
        self.is_callable()
