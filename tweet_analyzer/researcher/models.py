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
	def has_reached_request_limit(self, search_type):
		if search_type == '30Day':
			pass
		elif search_type == 'FullArchive':
			pass
		logger.error("Invalid Search Type: {0}".format(search_type))
		return True



def increment_login_count(sender, user, request, **kwargs):

	if getattr(request, 'user', None):
		researcher, created = Researcher.objects.get_or_create(account = user)
		researcher.login_count = researcher.login_count + 1
		researcher.save()


user_logged_in.connect(increment_login_count)
