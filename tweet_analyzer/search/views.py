
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from common.twitter import TwitterHelper, TwitterDataEncoder
import json


def search(request):
	return render(request, 'search/search.html')

def saved_search(request):
	return render(request, 'search/search.html')

def get_tweets(request):
	import pdb;pdb.set_trace()
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

