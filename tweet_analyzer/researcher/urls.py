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
    # url(r'new_invitation$', new_invitation, name="player_new_invitation"),
    # url(r'accept_invitation/(?P<id>\d+)/$',
    #     accept_invitation,
    #     name="player_accept_invitation"),
    # url(r'signup$', SignUpView.as_view(), name='player_signup'),
]