
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from common.twitter import TwitterHelper, TwitterDataEncoder
from django.views.generic import TemplateView
from django.conf import settings
import json
import csv


class Search(LoginRequiredMixin, TemplateView):
	template_name = 'search/search.html'
	redirect_field_name = 'welcome'
	login_url = 'researcher_login'


@login_required
def get_tweets(request):
	import pdb;pdb.set_trace()
	max_results = None
	searchq = None
	from_date = None
	to_date = None

	if request.GET['searchq']:
		searchq	= request.GET['searchq']
	if request.GET['fromDate']:
		from_date = request.GET['fromDate']
	if request.GET['toDate']:
		to_date = request.GET['toDate']
	twitter = TwitterHelper(searchq, from_date, to_date)
	twitter_response = twitter.get_tweets()
	if twitter_response['message'] and twitter_response['message'] != '':
		return HttpResponseBadRequest(twitter_response['message'])
	tweets = twitter_response['data']

	#consider getting rid of isExport. Data should probably always be an export rather than
	#raw data?  NOT SURE ABOUT THAT.  Raw data is good for eyeballing.
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

@login_required
def search_counts(request):
	import pdb;pdb.set_trace()
	max_results = None
	searchq = None
	from_date = None
	to_date = None

	if request.GET['searchq']:
		searchq	= request.GET['searchq']
	if request.GET['fromDate']:
		from_date = request.GET['fromDate']
	if request.GET['toDate']:
		to_date = request.GET['toDate']
	twitter = TwitterHelper(searchq, from_date, to_date)
	twitter_response = twitter.get_tweets()
	if twitter_response['message'] and twitter_response['message'] != '':
		return HttpResponseBadRequest(twitter_response['message'])
	tweets = twitter_response['data']

	#consider getting rid of isExport. Data should probably always be an export rather than
	#raw data?  NOT SURE ABOUT THAT.  Raw data is good for eyeballing.
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

