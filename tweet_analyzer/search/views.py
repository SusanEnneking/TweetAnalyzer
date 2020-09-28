
from django.http import HttpResponse
from django.http import JsonResponse
from common.twitter import TwitterHelper, TwitterDataEncoder
from django.views.generic import TemplateView
import json


class Search(TemplateView):
	template_name = 'search/search.html'

class SavedSearch(TemplateView):
	template_name = 'search/search.html'

def get_tweets(request):
	max_request_count = None
	searchq = None
	from_date = None
	to_date = None
	if request.GET['maxRequestCount']:
		max_request_count = request.GET['maxRequestCount']
	if request.GET['searchq']:
		searchq	= request.GET['searchq']
	if request.GET['fromDate']:
		from_date = request.GET['fromDate']
	if request.GET['toDate']:
		to_date = request.GET['toDate']
	twitter = TwitterHelper(max_request_count, searchq, from_date, to_date)
	tweets = twitter.get_tweets()
	json_string = json.dumps([tweet.__dict__ for tweet in tweets], cls=TwitterDataEncoder)
	return HttpResponse(json_string, content_type='application/json')

