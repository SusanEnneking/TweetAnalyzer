import requests
import unittest
from unittest import mock
from common.twitter import TwitterHelper
import json
from json import JSONEncoder
from django.conf import settings
import datetime
from datetime import datetime, timedelta
from urllib.parse import urlencode
import ast
from django.contrib.auth.models import User
from researcher.models import Researcher


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    if settings.OAUTH_ENDPOINT in args[0]:
        return MockResponse({"access_token": "You have been granted access"}, 200)

    return MockResponse(None, 404)


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, content, status_code, encoding):
            self.content = content
            self.status_code = status_code
            self.encoding = encoding

        def content(self):
            return self.content

    if settings.MONTH_ENDPOINT in args[0] or settings.FULL_ENDPOINT in args[0]:
        json_data = 'None'
        message = ''
        with open('common/test_data/test_response.json', 'rb') as json_file:
            json_data = json_file.read()

        return MockResponse(json_data, 200, 'utf-8')

    return MockResponse(None, 404)


def mocked_count_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, content, status_code, encoding):
            self.content = content
            self.status_code = status_code
            self.encoding = encoding

        def content(self):
            return self.content

    if settings.MONTH_COUNTS_ENDPOINT in args[0] or settings.FULL_COUNTS_ENDPOINT in args[0]:
        json_data = 'None'
        message = ''
        with open('common/test_data/test_count_response.json', 'rb') as json_file:
            json_data = json_file.read()

        return MockResponse(json_data, 200, 'utf-8')

    return MockResponse(None, 404)


class TwitterClassTestCase(unittest.TestCase):
    def setUp(self):
        self.user, created = User.objects.get_or_create(
            username='twitterTester', email='twittertester@tester.com', password='top_secret')
        self.researcher, created = Researcher.objects.get_or_create(account=self.user)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_search(self, mock_get, mock_post):
        searchq = 'RGB'
        from_date = None
        to_date = None
        bucket = None
        twitter = TwitterHelper(searchq, from_date, to_date, bucket, self.user)

        twitter_response = twitter.get_tweets()
        message = twitter_response['message']
        self.assertEqual(message, '')
        tweets = twitter_response['data']
        # The test_response.json file in mocked_requests_get contains 10 tweets
        self.assertEqual(len(tweets), 10)

    @mock.patch('requests.get', side_effect=mocked_count_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_counts(self, mock_get, mock_post):
        searchq = 'RGB'
        from_date = None
        to_date = None
        bucket = 'day'
        twitter = TwitterHelper(searchq, from_date, to_date, bucket, self.user)
        twitter_response = twitter.get_tweets()
        message = twitter_response['message']
        self.assertEqual(message, '')
        total_count = twitter_response['total_count']
        # The test_count_response.json file in mocked_count_requests_get totalCount = 1404
        self.assertEqual(total_count, 1404)


if __name__ == '__main__':
    unittest.main()
