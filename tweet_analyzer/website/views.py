

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def welcome(request):
	return render(request, 'website/welcome.html')

def about(request):
	return HttpResponse("Hi, my name is Susan Enneking \nI'm a developer with one foot in Django \n and one foot in C#")
