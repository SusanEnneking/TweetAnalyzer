
import logging
logger = logging.getlogger(__name__)
import requests

class twitter(object):

	def __init__(self):
		self.max_request_count


	def get_tweets(self):
		token  get_token()
		url = get_url()
		logger.info("Url: {0}".format(url))
		all_tweets = []
		max_request_count = self.max_request_count
		if ! max_request_count || max_request_count == 0:
			max_request_count = 1

		logger.info("Max Requests: {0}".format(max_request_count))
		access_token = token.access_token
		if token.token_type == 'bearer':
			call_count = 0
			more_tweets = true
			next_indicator = ''
			while (more_tweets && call_count < max_request_count)
				call_count = call_count + 1
				logger.info("Searching ...")
				tweets = search(access_token, next_indicator, url)
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

	def search(token, next, url):
		headers = {"Authorization": "TOK: {0}".format(token)}
		url = url + next
		request = requests.get(url, headers=headers)
