
import logging
logger = logging.getLogger('django')
import requests
import json
from json import JSONEncoder
from django.conf import settings
import datetime
from datetime import datetime, timedelta
from urllib.parse import urlencode
import ast



class TwitterHelper(object):

	def __init__(self, searchq, from_date, to_date, bucket):
		format = '%Y-%m-%dT%H:%M'
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



	def get_tweets(self):
		access_token = ''
		access_token = self.get_token()
		url = self.get_url()
		logger.debug("Url: {0}".format(url))
		all_tweets = []
		max_requests = self.max_requests
		logger.info("Max Results: {0}".format(max_requests))
		call_count = 0
		more_tweets = True
		next_indicator = ''
		error_message = ''
		while (more_tweets and call_count < max_requests):
			import pdb;pdb.set_trace()
			call_count = call_count + 1
			logger.info("Searching ...")
			tweets = self.search(access_token, next_indicator, url)
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
		import pdb;pdb.set_trace()
		return {'message': error_message, 'data': all_tweets, 'request_parameters': tweets.request_parameters, 'total_count': tweets.total_count}

	def search(self, token, next, url):
		headers = {"Authorization": "Bearer {0}".format(token)}
		url = url + next
		response = requests.get(url, headers=headers)
		json_data = None
		message = ''
		if response.status_code == 200:
			json_data = json.loads(response.content.decode(response.encoding))
			#to write this to a file for testing, put a breakpoint here, then use:
			# 	f = open('common/test_data/test_response.json', 'wb')
			#	f.write(response.content)
			#in shell to write a test file you can use in tests/test_search.py
		else:
			message = "Error: Status-{0} Message-{1} {2}".format(response.status_code, response.reason, response.text)
			logger.error(message)
		twitter_response = TwitterResponse({'message': message, 'data':json_data})
		return twitter_response

	def get_url(self):
		if self.bucket:
			url = settings.MONTH_COUNTS_ENDPOINT
		else:
			url = settings.MONTH_ENDPOINT
		thirty_days_ago = datetime.today() - timedelta(days=30)
		logger.info("Thirty days ago = {0}".format(thirty_days_ago))
		if self.from_date and self.from_date < thirty_days_ago or \
			self.to_date and self.to_date < thirty_days_ago:
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
		return url

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

class TwitterResponse(object):
	def __init__(self, data):
		self.message = data['message']
		self.results = []
		if 'data' in data:
			if 'next' in data['data']:
				self.next = data['data']['next']
			else:
				self.next = None
			if 'results' in data['data']:
				for result in data['data']['results']:
					if 'totalCount' in data['data']:
						tweet = TweetCountData(result)
						self.total_count = data['data']['totalCount']
					else:
						tweet = TweetData(result)
						self.total_count = 0
					self.results.append(tweet)
			self.request_parameters = data['data']['requestParameters']



class TweetData(object):

	def __init__(self, data):
		self.created_at = data['created_at']
		self.id_str = data['id_str']
		self.source = data['source']
		self.user = TwitterUser(data['user'])
		self.text = data['text']



class TwitterUser(object):
	#Twitter has much more data, this is just what Melody needed for her research
	def __init__(self, data):
		self.name = data['name']
		self.screen_name = data['screen_name']
		self.location = data['location']
		self.description = data['description']
		self.followers_count = data['followers_count']
		self.friends_count = data['friends_count']
		self.statuses_count = data['statuses_count']

class TweetCountData(object):

	def __init__(self, data):
		self.time_period = data['timePeriod']
		self.count = data['count']


class TwitterDataEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__



