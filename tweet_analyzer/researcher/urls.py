from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from researcher.forms import ResearcherLoginForm


urlpatterns = [
    url(r'login$',
        LoginView.as_view(template_name="researcher/login_form.html", authentication_form=ResearcherLoginForm),
        name="researcher_login"),
    url(r'logout$',
        LogoutView.as_view(),
        name="researcher_logout"),
]
