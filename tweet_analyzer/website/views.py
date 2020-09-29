
from django.views.generic import TemplateView


class Welcome(TemplateView):
	template_name = 'website/welcome.html'

class About(TemplateView):
	template_name = 'website/about.html'
