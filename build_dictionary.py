#!/usr/bin/python3
import json
import string
import re
from nltk.corpus import cmudict

cmudict = cmudict.dict()

# ------------------------------------------------------------------------------


def load_tweets(fname):
    # loads tweet timeline data, strips all unnecessary punctuation
    with open(fname) as f:
        tweets = f.read()
        tweets = re.sub(r'[^\w\s]', ' ', tweets)  # strips unicode punctuation
        tweets = set(tweets.split())
        return tweets

# ------------------------------------------------------------------------------


def find_cmu_missing(tweet_words):
    # return set of words in tweet.txt absent from cmudict
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
    allows user to filter out words to be omitted from final dictionary. Used 
    to remove any garbage, misspelled words, or general nonsense
    '''
    filtered_set = set()
    print('Enter n to remove word from set')
    for word in raw_missing_set:
        keep_status = input('\n%s\n' % word)
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
    print('Number of words in missing_words.txt: %s' % len(syllables))

    f = open('missing_dict.json', 'w')
    f.write(json.dumps(syllables))
    f.close()
    print('Saved to missing_dict.json')


# ------------------------------------------------------------------------------

def return_syllable_count(_string):
    with open('missing_dict.json', 'r') as f:
        missing_dict = json.load(f)

    words = re.sub(r'[^\w\s]', ' ', _string)
    words = words.lower().split()
    syllable_count = 0
    for word in words:
        if word in missing_dict:
            syllable_count += missing_dict[word]
        else:
            # iterate through first pronunciation of word ([0])
            for sounds in cmudict[word][0]:
                for sound in sounds:
                    if sound[-1].isdigit():
                        # if vowel, count as one syllable
                        syllable_count += 1
    print(syllable_count)
    return syllable_count


# ------------------------------------------------------------------------------


def main():
    '''
    tweets = load_tweets('tweets.txt')
    missing = find_cmu_missing(tweets)
    filtered = filter_missing(missing)
    make_missing_dict(filtered)
    '''
    pass
# ------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
