from django.conf.urls import url

from .views import Search, get_tweets

urlpatterns = [
    url(r'search$', Search.as_view(), name="search"),
    url(r'get_tweets$', get_tweets, name="get_tweets"),
    # url(r'new_invitation$', new_invitation, name="player_new_invitation"),
    # url(r'accept_invitation/(?P<id>\d+)/$',
    #     accept_invitation,
    #     name="player_accept_invitation"),
    # url(r'signup$', SignUpView.as_view(), name='player_signup'),
]