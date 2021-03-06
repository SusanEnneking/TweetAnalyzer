
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from common.twitter import TwitterHelper, TwitterDataEncoder
from django.views.generic import ListView
from django.conf import settings
import json
import csv
from search.models import Search


class SearchTweets(LoginRequiredMixin, ListView):
    template_name = 'search/search.html'
    redirect_field_name = 'welcome'
    login_url = 'researcher_login'
    model = Search

    def get_queryset(self):
        return Search.objects.filter(researcher__account=self.request.user).order_by("-query_time")


@login_required
def get_tweets(request):
    searchq = None
    from_date = None
    to_date = None
    searchq = request.GET.get('searchq', '')
    from_date = request.GET.get('fromDate', None)
    to_date = request.GET.get('toDate', None)
    bucket = request.GET.get('bucket', None)
    is_export = request.GET.get('isExport', None)
    twitter = TwitterHelper(searchq, from_date, to_date, bucket, request.user)
    twitter_response = twitter.get_tweets()
    if twitter_response['message'] and twitter_response['message'] != '':
        return HttpResponseBadRequest(twitter_response['message'])
    tweets = twitter_response['data']

    # consider getting rid of isExport. Data should probably always be an export rather than
    # raw data?  NOT SURE ABOUT THAT.  Raw data is good for eyeballing.
    if is_export and is_export == 'True':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tweets.csv"'

        writer = csv.writer(response, delimiter='|')
        writer.writerow(twitter.get_header())
        for tweet in tweets:
            writer.writerow(twitter.get_row(tweet))
        writer.writerow(['Query:{0}'.format(twitter_response['request_parameters'])])
        writer.writerow(['Count (0 if not a Count query):{0}'.format(twitter_response['total_count'])])
        return response
    else:
        json_string = json.dumps([tweet.__dict__ for tweet in tweets], cls=TwitterDataEncoder)
        return HttpResponse(json_string, content_type='application/json')


@login_required
def limit_reached(request):
    searchq = None
    from_date = None
    to_date = None
    searchq = request.GET.get('searchq', '')
    from_date = request.GET.get('fromDate', None)
    to_date = request.GET.get('toDate', None)
    bucket = request.GET.get('bucket', None)
    is_export = request.GET.get('isExport', None)
    twitter = TwitterHelper(searchq, from_date, to_date, bucket, request.user)
    return HttpResponse(twitter.limit_reached, status=200)
