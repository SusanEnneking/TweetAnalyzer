
import logging
logger = logging.getLogger(__name__)
import requests
import json
from json import JSONEncoder
from django.conf import settings
import datetime
from datetime import datetime, timedelta
from urllib.parse import urlencode
import ast



class TwitterHelper(object):

	def __init__(self, max_request_count, searchq, from_date, to_date):
		import pdb;pdb.set_trace()
		format = '%Y-%m-%dT%H:%M'
		self.date_string_format = '%Y%m%d%H%M'
		self.max_request_count = int(max_request_count)
		self.searchq = searchq
		self.from_date = datetime.strptime(from_date, format)
		self.to_date = datetime.strptime(to_date, format)
		self.max_results = 10


	def get_tweets(self):
		access_token = ''
		#access_token = self.get_token()
		url = self.get_url()
		logger.info("Url: {0}".format(url))
		all_tweets = []
		max_request_count = self.max_request_count
		if not max_request_count or max_request_count == 0:
			max_request_count = 1

		logger.info("Max Requests: {0}".format(max_request_count))
		call_count = 0
		more_tweets = True
		next_indicator = ''
		while (more_tweets and call_count < max_request_count):
			import pdb;pdb.set_trace()
			call_count = call_count + 1
			logger.info("Searching ...")
			tweets = self.search(access_token, next_indicator, url)
			if tweets.message == '' and tweets.results and len(tweets.results) > 0:
				all_tweets = all_tweets + tweets.results
				next_prop_exists = False
				if tweets.next and len(tweets.results) < self.max_results:
					next_prop_exists = True
				logger.info("Tweet Count...{0} Next... {1}".format(len(all_tweets), next_prop_exists))
				if next_prop_exists:
					next_indicator = "&next={0}".format(tweets.next)
				else:
					more_tweets = False
			else:
				logger.error("Twitter didn't return any data")
		import pdb;pdb.set_trace()
		return all_tweets

	def search(self, token, next, url):
		# headers = {"Authorization": "Bearer {0}".format(token)}
		# url = url + next
		# response = requests.get(url, headers=headers)
		json_data = 'None'
		message = ''
		# if response.status_code == 200:
		# 	resp = json.loads(response.content.decode(response.encoding))
		# else:
		# 	message = "Error: Status-{0} Message-{1} {2}".format(response.status_code, response.reason, response.text)
		# 	logger.error(message)
		with open('common/test_data/test_response.json') as json_file:
			json_data = json_file.read()
			json_data = ast.literal_eval(json_data)
		twitter_response = TwitterResponse({'message': message, 'data':json_data})
		return twitter_response

	def get_url(self):
		url = settings.MONTH_ENDPOINT
		thirty_days_ago = datetime.today() - timedelta(days=30)
		logger.info("Thirty days ago = {0}".format(thirty_days_ago))
		if self.from_date and self.from_date < thirty_days_ago or \
		   self.to_date and self.to_date < thirty_days_ago:
		   logger.info("From date: {0}".format(self.from_date))
		   logger.info("To date: {0}".format(self.to_date))
		   logger.info("From or to date less than 30 days ago, using full archive endpoint")
		   url = settings.FULL_ENDPOINT
		else:
			logger.info("From and to dates are within 30 days, using 30 day endpoint")

		url = "{0}?query={1}".format(url, self.searchq)
		if self.from_date:
			url = "{0}&fromDate={1}".format(url, self.from_date.strftime(self.date_string_format))

		if self.to_date:
			url = "{0}&toDate={1}".format(url, self.to_date.strftime(self.date_string_format))

		url = "{0}&maxResults={1}".format(url, self.max_results)
		return url

	def get_token(self):
		data = [('grant_type', 'client_credentials')]
		response = requests.post(settings.OAUTH_ENDPOINT, auth=(settings.CONSUMER_KEY, settings.CONSUMER_SECRET), data=data)
		json_data = response.json()
		return json_data['access_token']

class TwitterResponse(object):
	def __init__(self, data):
		self.message = data['message']
		self.next = data['data']['next']
		self.results = []
		for result in data['data']['results']:
			tweet = TweetData(result)
			self.results.append(tweet)
		self.request_parameters = data['data']['requestParameters']



class TweetData(object):
	#Twitter has much more data, this is just what Melody needed for her research
	def __init__(self, data):
		self.created_at = data['created_at']
		self.id_str = data['id_str']
		self.source = data['source']
		self.user = TwitterUser(data['user'])
		self.text = data['text']



class TwitterUser(object):
	def __init__(self, data):
		self.name = data['name']
		self.screen_name = data['screen_name']
		self.location = data['location']
		self.description = data['description']
		self.followers_count = data['followers_count']
		self.friends_count = data['friends_count']
		self.statuses_count = data['statuses_count']

class TwitterDataEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__



