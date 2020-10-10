from django.conf.urls import url

from .views import SearchTweets, get_tweets, limit_reached

urlpatterns = [
    url(r'search$', SearchTweets.as_view(), name="search"),
    url(r'get_tweets$', get_tweets, name="get_tweets"),
    url(r'limit_reached$', limit_reached, name="limit_reached"),
    # url(r'new_invitation$', new_invitation, name="player_new_invitation"),
    # url(r'accept_invitation/(?P<id>\d+)/$',
    #     accept_invitation,
    #     name="player_accept_invitation"),
    # url(r'signup$', SignUpView.as_view(), name='player_signup'),
]
