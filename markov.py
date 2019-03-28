import json
import re
import random
from collections import defaultdict
from nltk.corpus import cmudict
from build_dictionary import load_tweets

cmudict = cmudict.dict()

# -----------------------------------------------------------------------------


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


def select_seed(k1_chain, max_syl=4):
    '''
    takes in chain k=1 generated from make_markov_chain(), seeds haiku
    '''
    invalid_syl = True
    while invalid_syl:
        seed = random.choice(list(k1_chain))
        num_syl = return_syllable_count(seed)
        if num_syl <= max_syl:
            invalid_syl = False
            return seed

# -----------------------------------------------------------------------------


def choose_second_word(seed, k1_chain, max_syl=5):
    '''
    chooses second word in haiku to start k=2 markov chain seeding
    '''
    seed_syl = return_syllable_count(seed)
    next_words = k1_chain.get(seed)

    syl_count = seed_syl
    valid_words = []
    for word in next_words:
        print(word)
        syl = return_syllable_count(word)
        if seed_syl + syl <= max_syl:
            valid_words.append(word)
    print(valid_words)


# -----------------------------------------------------------------------------
tweets = load_tweets('final_tweets.txt', return_set=False)
k1 = make_markov_chain(tweets, 1)
seed = select_seed(k1)
print(seed)
choose_second_word(seed, k1)
