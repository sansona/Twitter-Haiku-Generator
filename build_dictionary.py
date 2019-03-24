#!/usr/bin/python3
import json
import string
from nltk.corpus import cmudict

cmudict = cmudict.dict()

# ------------------------------------------------------------------------------


def load_tweets(fname):
    # loads tweet timeline data, strips all unnecessary punctuation
    with open(fname) as f:
        # (TODO): implement more effective method of stripping punctuation
        tweets = f.read().translate(
            str.maketrans('', '', string.punctuation))
        tweets = set(tweets.split())
        return tweets

# ------------------------------------------------------------------------------


def find_cmu_missing(tweet_words):
    # return set of words in tweet.txt missing from cmudict
    missing_words = set()
    for word in tweet_words:
        word = word.lower()
        if word not in cmudict:
            missing_words.add(word)
    print('Number unique words in tweets: %s' % len(tweet_words))
    print('Number missing words from CMUdict: %s' % len(missing_words))

    return missing_words

# ------------------------------------------------------------------------------


def filter_missing(raw_missing_set):
    '''
    allows user to select appropriate words in missing_words to ensure all in
    set are real words
    '''
    filtered_set = set()
    print('Enter n to remove word from set')
    for word in raw_missing_set:
        keep_status = input('%s\n' % word)
        if keep_status != 'n':
            filtered_set.add(word)

    print('Words filtered from set: %s' %
          (len(raw_missing_set)-len(filtered_set)))

    return filtered_set


# ------------------------------------------------------------------------------


def make_missing_dict(set_missing_words):
    # creates and returns dict of missing words & syllables via. user input
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
    print(syllables)
    print('Number of words in missing_words.txt: %s' % len(syllables))

    # saves missing words
    f = open('missing_dict.json', 'w')
    f.write(json.dumps(syllables))
    f.close()
    print('\nMissing words saved to missing_dict.jsonn')


# ------------------------------------------------------------------------------


def main():
    # load tweets
    tweets = load_tweets('tweets.txt')
    # find missing from cmu
    missing = find_cmu_missing(tweets)
    # make missing dict
    filtered = filter_missing(missing)
    # make_missing_dict(filtered)

# ------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
