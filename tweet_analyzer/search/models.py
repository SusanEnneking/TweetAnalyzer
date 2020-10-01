from django.db import models
from researcher.models import Researcher

class Search(models.Model):
	researcher = models.ForeignKey(Researcher, related_name="researcher", on_delete=models.SET_NULL, null=True)
	#note, Sandbox max query length is 256
	query = models.CharField(max_length=1024, default='')
	from_date = models.DateTimeField()
	to_date = models.DateTimeField()
	query_time =models.DateTimeField(auto_now_add=True)
	twitter_response_status = models.CharField(max_length=3, default='')
	query_url = models.CharField(max_length=1500, default='')
	count = models.IntegerField(default=0)
	data_count = models.IntegerField(default=0)
	message = models.CharField(max_length=2000, default='')
