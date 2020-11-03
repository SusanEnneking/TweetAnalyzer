class TwitterResponse(object):
    def __init__(self, data):
        self.message = data['message']
        self.results = []
        self.total_count = 0
        self.next = None
        self.request_parameters = None
        if 'data' in data and data['data'] is not None:
            if 'next' in data['data']:
                self.next = data['data']['next']
            else:
                self.next = None
            if 'results' in data['data']:
                for result in data['data']['results']:
                    if 'totalCount' in data['data']:
                        tweet = TweetCountData(result)
                        self.total_count = data['data']['totalCount']
                    else:
                        tweet = TweetData(result)
                        self.total_count = 0
                    self.results.append(tweet)
            self.request_parameters = data['data']['requestParameters']


class TweetData(object):

    def __init__(self, data):
        self.created_at = data['created_at']
        self.id_str = data['id_str']
        self.source = data['source']
        self.user = TwitterUser(data['user'])
        self.text = data['text']


class TwitterUser(object):
    # Twitter has much more data, this is just what Melody needed for her research
    def __init__(self, data):
        self.name = data['name']
        self.screen_name = data['screen_name']
        self.location = data['location']
        self.description = data['description']
        self.followers_count = data['followers_count']
        self.friends_count = data['friends_count']
        self.statuses_count = data['statuses_count']


class TweetCountData(object):

    def __init__(self, data):
        self.time_period = data['timePeriod']
        self.count = data['count']

