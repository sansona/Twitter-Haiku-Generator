#!/usr/bin/python3
import json
import re
from nltk.corpus import cmudict

# -----------------------------------------------------------------------------
# Collection of functions for setting up cmudict & syllable counting functions
# for determining syllable count of all words in word collection
# -----------------------------------------------------------------------------

cmudict = cmudict.dict()

# -----------------------------------------------------------------------------


def load_tweets(fname, return_set=True):
    '''
    loads tweet timeline data, formats data (strip punctuation & forces lower
    case. Returns list of tweets or set of words
    '''
    with open(fname) as f:
        tweets = f.read().lower()
        tweets = re.sub(r'[^\w\s]', ' ', tweets)  # strips unicode punctuation
        if return_set:
            tweets = set(tweets.split())
        else:
            tweets = tweets.split()
        return tweets

# -----------------------------------------------------------------------------


def find_cmu_missing(tweet_words):
    '''
    return set of words in tweet.txt absent from cmudict. Set of words will
    likely be comprised of slang, misspellings, or anything not unusually in
    a dictionary
    '''
    missing_words = set()
    for word in tweet_words:
        word = word.lower()
        if word not in cmudict and not word.isdigit():
            missing_words.add(word)
    print('Number unique words in tweets: %s' % len(tweet_words))
    print('Number missing words from CMUdict: %s' % len(missing_words))

    return missing_words

# -----------------------------------------------------------------------------


def filter_missing(raw_missing_set):
    '''
    allows user to filter out words to be omitted from final dictionary. Used
    to remove any garbage, misspelled words, or general nonsense
    '''
    filtered_set = set()
    removed_words = []
    print('Enter n to remove word from set')
    for word in raw_missing_set:
        keep_status = input('\n%s\n' % word)
        if keep_status != 'n':
            filtered_set.add(word)
        else:
            removed_words.append(word)
    print('Words filtered from set: %s' %
          (len(raw_missing_set)-len(filtered_set)))

    return filtered_set, removed_words


# -----------------------------------------------------------------------------

def extract_removed_words(removed_words):
    '''
    creates final .txt with words that were flagged in filter_missing and
    words deemed inappropriate for haikus (too long or containing digits)
    '''
    raw_tweets = load_tweets('tweets.txt', return_set=False)
    for word in raw_tweets:
        if word in removed_words:
            # raw_tweets.remove(word)
            raw_tweets = [x for x in raw_tweets if x != word]
        elif any(char.isdigit() for char in word):
            raw_tweets.remove(word)
        elif len(word) > 10:
            raw_tweets.remove(word)

    with open('final_tweets.txt', 'w') as f:
        for tweet in raw_tweets:
            f.write('%s\n' % tweet)

# -----------------------------------------------------------------------------


def make_missing_dict(set_missing_words):
    '''
    utilizes words deemed to be usable from filter_missing and creates
    .json dict with syllable count as value via. user input
    '''
    syllables = {}
    print('Enter number of syllables')

    recording_counts = True
    for word in set_missing_words:
        while recording_counts:
            num_syllables = input('Number syllables in %s\n' % word)
            if num_syllables.isdigit():
                break
            else:
                print('Not valid input')
                continue
        syllables[word] = int(num_syllables)
    print('Number of words in missing_words.txt: %s' % len(syllables))

    f = open('missing_dict.json', 'w')
    f.write(json.dumps(syllables))
    f.close()
    print('Saved to missing_dict.json')

# -----------------------------------------------------------------------------


def build_new_dict():
    '''
    pipeline for converting tweets.txt to final_tweets.txt (unwanted words
    filtered out) and missing_dict.json (syllable counts of words kept)
    '''
    tweets = load_tweets('tweets.txt')
    missing = find_cmu_missing(tweets)
    filtered, removed = filter_missing(missing)

    extract_removed_words(removed)  # makes new txt without unwanted words
    make_missing_dict(filtered)

# -----------------------------------------------------------------------------
