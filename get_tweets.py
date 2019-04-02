import twitter

# NOTE: there's python-twitter & twitter. pip install python-twitter for
# correct package

# -----------------------------------------------------------------------------
# ----------------------FILL THIS OUT BEFORE RUNNING---------------------------

APP_KEY = ''
APP_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET,
                  APP_KEY, APP_SECRET)

# -----------------------------------------------------------------------------


def scrape_timeline(user, n=30):
    '''
    scrape most recent n tweets from user timeline, writes to txt file
    .txt still has to be processed before use

    NOTE: Twitter limits scraping 200 tweets/request. To get around
    this limit, can send multiple spaced out requests
    '''
    statuses = api.GetUserTimeline(screen_name=user, count=n)
    tweets = [status.text for status in statuses]
    tweets = [t[:-23] for t in tweets]  # strip auto-included URL from tweet

    with open('tweets.txt', 'w') as f:
        for tweet in tweets:
            f.write('%s\n' % tweet)

# -----------------------------------------------------------------------------


def post_tweet(haiku, user):
    '''
    formats haiku from list to haiku strings, posts to Twitter
    '''
    haiku_str = 'from %s:\n\n' % user
    for line in haiku:
        haiku_str += str(line[0])
        haiku_str += '\n'

    status = api.PostUpdate(haiku_str)

# -----------------------------------------------------------------------------
