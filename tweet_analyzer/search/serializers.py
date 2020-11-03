# todo/serializers.py

from rest_framework import serializers
from common import TwitterResponses

class TwitterUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    screen_name = serializers.CharField(max_length=200)
    location = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    followers_count = serializers.IntegerField()
    friends_count = serializers.IntegerField()
    statuses_count = serializers.IntegerField()

class TwitterResponseSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField()
    id_str = serializers.CharField(max_length=50)
    source = serializers.CharField(max_length=200)
    user = TwitterUserSerializer()
    text = serializers.CharField(max_length=144)

class TwitterCountDataSerializer(serializers.Serializer):
	time_period = serializers.CharField(max_length=100)
	count = serializers.IntegerField()


		
   