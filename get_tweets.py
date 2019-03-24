import twitter

# NOTE: there's python-twitter & twitter. pip install python-twitter for
# correct package

APP_KEY = ''
APP_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET,
                  APP_KEY, APP_SECRET)

statuses = api.GetUserTimeline(screen_name='', count=200)
tweets = [status.text for status in statuses]
tweets = [t[:-23] for t in tweets]  # strip auto-included URL from tweet

with open('tweets.txt', 'w') as f:
    for tweet in tweets:
        f.write('%s\n' % tweet)
