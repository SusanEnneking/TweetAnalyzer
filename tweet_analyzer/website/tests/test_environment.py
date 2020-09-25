

from django.test import TestCase
import os

class VerifyEnvironmentSettings(TestCase):

	def test_environment_set(self):
		ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT")
		self.assertNotEqual(ENVIRONMENT, None)

	def test_secret_key_set(self):
		SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
		self.assertNotEqual(SECRET_KEY, None)

	def test_consumer_key_set(self):
		CONSUMER_KEY = os.getenv('CONSUMER_KEY')
		self.assertNotEqual(CONSUMER_KEY, None)

	def test_consumer_secret_set(self):
		CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
		self.assertNotEqual(CONSUMER_SECRET, None)

	def test_app_name_set(self):
		TWITTER_APP_NAME = os.getenv('TWITTER_APP_NAME')
		self.assertNotEqual(TWITTER_APP_NAME, None)
