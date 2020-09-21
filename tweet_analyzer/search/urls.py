from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from .views import search, saved_search

urlpatterns = [
    url(r'search$', search, name="search"),
    url(r'saved_search$', saved_search, name="saved_search")
    # url(r'login$',
    #     LoginView.as_view(template_name="player/login_form.html"),
    #     name="user_login"),
    # url(r'logout$',
    #     LogoutView.as_view(),
    #     name="user_logout"),
    # url(r'new_invitation$', new_invitation, name="player_new_invitation"),
    # url(r'accept_invitation/(?P<id>\d+)/$',
    #     accept_invitation,
    #     name="player_accept_invitation"),
    # url(r'signup$', SignUpView.as_view(), name='player_signup'),
]