from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
import pytz
import logging
logger = logging.getLogger('django')



class Researcher(models.Model):
	TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
	account = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
	login_count = models.IntegerField(default=0)
	time_zone = models.CharField(max_length=100, blank=True, null=True, choices=TIMEZONES, default='America/Chicago')
	request_limit_30day = models.IntegerField(default=0)
	request_limit_fullarchive = models.IntegerField(default=0)

	@property
	def has_reached_30day_limit(self):
		used = self.search_set.filter(researcher__id = self.id, query_url__icontains='30day')
		return self.request_limit_30day <= used.count()


	@property
	def has_reached_fullarchive_limit(self):
		used = self.search_set.filter(researcher__id = self.id, query_url__icontains='fullarchive')
		return self.request_limit_fullarchive <= used.count()

	def __str__(self):
		return self.account.email

def increment_login_count(sender, user, request, **kwargs):

	if getattr(request, 'user', None):
		researcher, created = Researcher.objects.get_or_create(account = user)
		researcher.login_count = researcher.login_count + 1
		researcher.save()


user_logged_in.connect(increment_login_count)
