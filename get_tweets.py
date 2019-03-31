import twitter

# NOTE: there's python-twitter & twitter. pip install python-twitter for
# correct package

APP_KEY = ''
APP_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET,
                  APP_KEY, APP_SECRET)

# -----------------------------------------------------------------------------


def scrape_tweets(user, COUNT=200):
    statuses = api.GetUserTimeline(screen_name=user, count=COUNT)
    tweets = [status.text for status in statuses]
    tweets = [t[:-23] for t in tweets]  # strip auto-included URL from tweet

    with open('tweets.txt', 'w') as f:
        for tweet in tweets:
            f.write('%s\n' % tweet)

# -----------------------------------------------------------------------------


def post_tweet(haiku, user):

    haiku_str = 'from %s:\n\n' % user
    for line in haiku:
        haiku_str += str(line[0])
        haiku_str += '\n'

    status = api.PostUpdate(haiku_str)

# -----------------------------------------------------------------------------
