import json
import re
import random
from collections import defaultdict
from nltk.corpus import cmudict
from build_dictionary import load_tweets

cmudict = cmudict.dict()

# -----------------------------------------------------------------------------


def return_syllable_count(_string):
    if type(_string) == list:
        _string = ' '.join(_string)

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


def seed_second_word(seed, k1_chain, max_syl=5):
    '''
    chooses second word in haiku to start k=2 markov chain seeding
    '''
    seed_syl = return_syllable_count(seed)
    next_words = k1_chain.get(seed)

    valid_words = []
    for word in next_words:
        syl = return_syllable_count(word)
        if seed_syl + syl <= max_syl:
            valid_words.append(word)

    return random.choice(valid_words)

# -----------------------------------------------------------------------------


def choose_next_word(line, k_chain, curr_syl, max_syl=5):
    if type(line) == str:
        key = line
    else:
        key = line[-2] + ' ' + line[-1]

    next_words = k_chain.get(key)
    valid_words = []
    for word in next_words:
        syl = return_syllable_count(word)
        if curr_syl + syl <= max_syl:
            valid_words.append(word)

    try:
        return random.choice(valid_words)
    except IndexError:
        # if no valid matches
        legal_syl = False
        while not legal_syl:
            next_words = random.choice(list(k_chain))
            valid_words = []
            for word in next_words:
                syl = return_syllable_count(word)
                if curr_syl + syl == max_syl:
                    valid_words.append(word)
                    legal_syl = True
                else:
                    continue
            return random.choice(valid_words)
# -----------------------------------------------------------------------------


def write_haiku(k1, k2, line_length=[5, 7, 5]):
    seed = select_seed(k1)
    second = seed_second_word(seed, k1)
    first_line = [seed, second]
    n_syl = return_syllable_count(first_line)
    while n_syl < line_length[0]:
        next_word = choose_next_word(first_line, k2, n_syl)
        first_line.append(next_word)
        n_syl += return_syllable_count(next_word)
    print(first_line)


# -----------------------------------------------------------------------------
tweets = load_tweets('final_tweets.txt', return_set=False)
k1 = make_markov_chain(tweets, 1)
k2 = make_markov_chain(tweets, 2)
for i in range(50):
    # next step: figure out how to fix these indexerrors
    try:
        write_haiku(k1, k2)
    except IndexError:
        print('Index error')
    except KeyError:
        print('Key error')
