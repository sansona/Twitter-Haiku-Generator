#!/usr/bin/python3
from get_tweets import *
from build_dictionary import *
from markov import *

import sys
import os
import argparse

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates haikus from user timeline data'
        ' via. Markov chains')
    parser.add_argument(
        'user', help='User data to generate model from', type=str)
    parser.add_argument('-n', '--new_dict', help='Build new dictionary?',
                        action='store_true')
    args = parser.parse_args()

    if args.new_dict:
        if not os.path.exists(args.user):
            os.makedirs(args.user)
        os.chdir(args.user)

        print('Scraping and generating dictionary...\n')
        scrape_tweets(args.user, 200)
        build_new_dict()
    else:
        os.chdir(args.user)

    good_haiku = False
    while not good_haiku:
        haiku = generate_models()
        post = input('Post?\n%s\n' % haiku)
        if post == 'y':
            post_tweet(haiku, user=args.user)
            good_haiku = True
