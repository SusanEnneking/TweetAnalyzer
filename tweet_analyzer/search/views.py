
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from common.twitter import TwitterHelper, TwitterDataEncoder
from django.views.generic import TemplateView
import json
import csv


class Search(TemplateView):
	template_name = 'search/search.html'

class SavedSearch(TemplateView):
	template_name = 'search/search.html'

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
	twitter_response = twitter.get_tweets()
	if twitter_response['message'] and twitter_response['message'] != '':
		return HttpResponseBadRequest(twitter_response['message'])
	tweets = twitter_response['data']
	if request.GET['isExport'] and request.GET['isExport'] == 'True':
	    response = HttpResponse(content_type='text/csv')
	    response['Content-Disposition'] = 'attachment; filename="tweets.csv"'

	    writer = csv.writer(response, delimiter='|')
	    writer.writerow(twitter.get_header())
	    for tweet in tweets:
	    	writer.writerow(twitter.get_row(tweet))
	    return response
	else:
		json_string = json.dumps([tweet.__dict__ for tweet in tweets], cls=TwitterDataEncoder)
		return HttpResponse(json_string, content_type='application/json')

