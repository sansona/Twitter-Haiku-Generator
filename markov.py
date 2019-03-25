import json
import re
from collections import defaultdict
from nltk.corpus import cmudict
from build_dictionary import load_tweets

cmudict = cmudict.dict()

# -----------------------------------------------------------------------------


def return_syllable_count(_string):
    with open('missing_dict.json', 'r') as f:
        missing_dict = json.load(f)

    words = re.sub(r'[^\w\s]', ' ', _string)
    words = words.upper().split()
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

# -----------------------------------------------------------------------------


def make_markov_chain(tweets, k):
    stop_count = len(tweets) - k
    dict_k = defaultdict(list)
    for i, word in enumerate(tweets):
        if k == 1:
            if i < stop_count:
                next_word = tweets[i+k]
                dict_k[word].append(next_word)

        elif k == 2:
            if i < stop_count:
                phrase = word + ' ' + tweets[i+1]
                next_word = tweets[i+k]
                dict_k[phrase].append(next_word)
    return dict_k


# -----------------------------------------------------------------------------
tweets = load_tweets('final_tweets.txt', return_set=False)
k1 = make_markov_chain(tweets, 2)
print(k1)
