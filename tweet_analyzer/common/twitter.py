
import logging
import requests
import json
import pytz
import ast
import datetime
from datetime import datetime, timedelta
from json import JSONEncoder
from django.conf import settings

from django.utils import timezone
from django.utils.timezone import make_aware
from urllib.parse import urlencode
from rest_framework.renderers import JSONRenderer
from search.models import Search
from common.TwitterResponses import TwitterResponse
from researcher.models import Researcher
from search.serializers import (TwitterUserSerializer, TwitterResponseSerializer,
                                TwitterCountDataSerializer)
logger = logging.getLogger('django')


class TwitterHelper(object):

    def __init__(self, searchq, from_date, to_date, bucket, user):
        format = '%Y-%m-%dT%H:%M'
        self.search_type = '30day'
        self.date_string_format = '%Y%m%d%H%M'
        self.max_requests = settings.MAX_REQUESTS
        self.max_results = settings.MAX_RESULTS
        self.searchq = searchq
        if from_date:
            self.from_date = datetime.strptime(from_date, format)
        else:
            self.from_date = None
        if to_date:
            self.to_date = datetime.strptime(to_date, format)
        else:
            self.to_date = None
        if bucket:
            self.bucket = bucket
        else:
            self.bucket = None
        self.researcher = Researcher.objects.get(account__id=user.id)
        self.set_url()
        self.set_search_type()

    @property
    def limit_reached(self):
        if self.search_type and self.search_type == '30Day':
            return self.researcher.has_reached_30day_limit
        elif self.search_type and self.search_type == 'FullArchive':
            return self.researcher.has_reached_fullarchive_limit
        return True

    def get_tweets(self):
        access_token = ''
        access_token = self.get_token()
        logger.debug("Url: {0}".format(self.url))
        all_tweets = []
        max_requests = self.max_requests
        logger.info("Max Results: {0}".format(max_requests))
        call_count = 0
        more_tweets = True
        next_indicator = ''
        error_message = ''
        while (more_tweets and call_count < max_requests):
            if (call_count > 1):
                # import pdb;pdb.set_trace()
                pass
            call_count = call_count + 1
            logger.info("Searching ...")
            tweets = self.search(access_token, next_indicator)
            if tweets.message == '' and tweets.results and len(tweets.results) > 0:
                all_tweets = all_tweets + tweets.results
                next_prop_exists = False
                if tweets.next:
                    next_prop_exists = True
                logger.info("Tweet Count...{0} Next... {1}".format(len(all_tweets), next_prop_exists))
                if next_prop_exists:
                    next_indicator = "&next={0}".format(tweets.next)
                else:
                    more_tweets = False
            else:
                logger.error("Twitter didn't return any data. Message: {0}".format(tweets.message))
                error_message = tweets.message
                break
        return {'message': error_message, 'data': all_tweets, 'request_parameters': tweets.request_parameters, 'total_count': tweets.total_count}

    def search(self, token, next):
        headers = {"Authorization": "Bearer {0}".format(token)}
        url = self.url + next
        response = requests.get(url, headers=headers)
        json_data = None
        import pdb;pdb.set_trace()
        message = ''
        if response.status_code == 200:
            json_data = json.loads(response.content.decode(response.encoding))
            # to write this to a file for testing, put a breakpoint here, then use:
            #   f = open('common/test_data/test_response.json', 'wb')
            #   f.write(response.content)
            # in shell to write a test file you can use in tests/test_search.py
        else:
            message = "Error: Status-{0} Message-{1} {2}".format(response.status_code, response.reason, response.text)
            logger.error(message)

        twitter_response = TwitterResponse({'message': message, 'data': json_data})

        search_info = Search.objects.create(
            researcher=self.researcher,
            query=twitter_response.request_parameters,
            from_date=self.from_date,
            to_date=self.to_date,
            query_time=timezone.now(),
            twitter_response_status=response.status_code,
            query_url=url,
            count=twitter_response.total_count,
            data_count=len(twitter_response.results),
            message=twitter_response.message
        )

        return twitter_response

    def set_url(self):

        if self.bucket:
            url = settings.MONTH_COUNTS_ENDPOINT
        else:
            url = settings.MONTH_ENDPOINT
        thirty_days_ago = timezone.now() - timedelta(days=30)
        tz = pytz.timezone(self.researcher.time_zone)
        if (self.from_date):
            self.from_date = tz.normalize(tz.localize(self.from_date)).astimezone(pytz.utc)
        if (self.to_date):
            self.to_date = tz.normalize(tz.localize(self.to_date)).astimezone(pytz.utc)
        logger.info("Thirty days ago = {0}".format(thirty_days_ago))
        if self.from_date and self.from_date < thirty_days_ago or self.to_date and self.to_date < thirty_days_ago:
            logger.info("From date: {0}".format(self.from_date))
            logger.info("To date: {0}".format(self.to_date))
            logger.info("From or to date less than 30 days ago, using full archive endpoint")
            if self.bucket:
                url = settings.FULL_COUNTS_ENDPOINT
            else:
                url = settings.FULL_ENDPOINT
        else:
            logger.info("From and to dates are within 30 days, using 30 day endpoint")

        url = "{0}?query={1}".format(url, self.searchq)
        if self.from_date:
            url = "{0}&fromDate={1}".format(url, self.from_date.strftime(self.date_string_format))

        if self.to_date:
            url = "{0}&toDate={1}".format(url, self.to_date.strftime(self.date_string_format))
        if self.bucket:
            url = "{0}&bucket={1}".format(url, self.bucket)
        else:
            url = "{0}&maxResults={1}".format(url, self.max_results)
        self.url = url

    def set_search_type(self):
        if settings.FULL_LITERAL in self.url:
            self.search_type = 'FullArchive'
        else:
            self.search_type = '30Day'

    def get_token(self):
        data = [('grant_type', 'client_credentials')]
        response = requests.post(settings.OAUTH_ENDPOINT, auth=(settings.CONSUMER_KEY, settings.CONSUMER_SECRET), data=data)
        json_data = response.json()
        return json_data['access_token']

    def get_row(self, tweet):
        if self.bucket:
            return [tweet.time_period, tweet.count]
        else:
            return [tweet.created_at, tweet.id_str, tweet.source, tweet.text,
                    tweet.user.name, tweet.user.screen_name, tweet.user.location,
                    tweet.user.description, tweet.user.followers_count,
                    tweet.user.friends_count, tweet.user.statuses_count]

    def get_header(self):
        if self.bucket:
            return ['Time Period', 'Count']
        else:
            return ['Created At', 'Id Str', 'Source', 'Text',
                    'User Name', 'User Screen Name', 'User Location',
                    'User Description', 'User Follower Count',
                    'User Friend Count', 'User Statuses Count']

    def serialize_data(self, tweets):
        import pdb;pdb.set_trace()
        if self.bucket:
            serializer = TwitterCountDataSerializer(tweets, many=True)
        else:
            serializer = TwitterResponseSerializer(tweets, many=True)
        json = JSONRenderer().render(serializer.data)
        return json


