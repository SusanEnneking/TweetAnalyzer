
import logging
logger = logging.getLogger(__name__)
import requests
import json
from django.conf import settings
import datetime
from datetime import datetime, timedelta
from urllib.parse import urlencode

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
		import pdb;pdb.set_trace()
		access_token = self.get_token()
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
			call_count = call_count + 1
			logger.info("Searching ...")
			tweets = self.search(access_token, next_indicator, url)
			if tweets.results:
				all_tweets = all_tweets + tweets.results
				next_prop_exists = False
				if tweets.next:
					next_prop_exists = True
				logger.info("Tweet Count...{0} Next... {1}".format(len(all_tweets)), next_prop_exists)
				if tweets.next:
					next_indicator = "&next={0}".format(tweets.next)
				else:
					more_tweets = False
			else:
				logger.error("Twitter didn't return any data")
		return all_tweets

	def search(self, token, next, url):
		import pdb;pdb.set_trace()
		headers = {"Authorization": "Bearer {0}".format(token)}
		url = url + next
		response = requests.get(url, headers=headers)
		json_data = 'None'
		if response.status_code == 200:
			resp = json.loads(response.content.decode(response.encoding))
		else:
			logger.error("Error: Status-{0} Message-{1} {2}".format(response.status_code, response.reason, response.text))
		return json_data

	def get_url(self):
		import pdb;pdb.set_trace()
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
