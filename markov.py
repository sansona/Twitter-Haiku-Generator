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


def choose_next_word(seed, k_chain, curr_syl, max_syl=5):
    '''
    takes in seed, traverses k_chain to return next word.
    If no valid next word, randomly select new seed and return traversal
    results from that seed
    '''
    if type(seed) == str:
        key = seed
    else:
        if len(seed) == 1:
            key = str(seed)
        else:
            key = seed[-2] + ' ' + seed[-1]

    next_words = k_chain.get(key)
    valid_words = []
    for word in next_words:
        syl = return_syllable_count(word)
        if curr_syl + syl <= max_syl:
            valid_words.append(word)

    if len(valid_words) > 0:
        return random.choice(valid_words)
    else:
        # if no valid matches for oriinal seed
        legal_syl = False
        while not legal_syl:
            # randomly choose seed return next in chain.
            # NOTE: does not replace original two words, only uses new words
            # as seed
            new_seeds = random.choice(list(k_chain))
            next_words = k_chain.get(new_seeds)
            valid_words = []
            for word in next_words:
                syl = return_syllable_count(word)
                if curr_syl + syl == max_syl:
                    valid_words.append(word)
                    legal_syl = True

        return random.choice(valid_words)
# -----------------------------------------------------------------------------


def write_haiku(k1, k2, line_length=[5, 7, 5]):
    seed = select_seed(k1)
    second = choose_next_word(seed, k1, return_syllable_count(seed))
    first_line = [seed, second]
    n_syl = return_syllable_count(first_line)
    while n_syl < line_length[0]:
        next_word = choose_next_word(first_line, k2, n_syl)
        first_line.append(next_word)
        n_syl += return_syllable_count(next_word)

    # This is a mess, working on cleaning this up
    second_seed = [first_line[-2], first_line[-1]]
    second_line_0 = choose_next_word(second_seed, k2, 0)
    second_line = [second_line_0]
    n2_syl = return_syllable_count(second_line)
    while n2_syl < line_length[1]:
        next_word = choose_next_word(second_line, k2, n_syl)
        second_line.append(next_word)
        n_syl += return_syllable_count(next_word)
    print(second_line)


# -----------------------------------------------------------------------------
tweets = load_tweets('final_tweets.txt', return_set=False)
k1 = make_markov_chain(tweets, 1)
k2 = make_markov_chain(tweets, 2)

key_cnt = 0
for i in range(500):
    try:
        write_haiku(k1, k2)
    except KeyError:
        key_cnt += 1
        print('Key error')
print(key_cnt)
