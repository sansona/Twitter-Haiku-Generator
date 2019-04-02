#!/usr/bin/python3
import os
import argparse

from get_tweets import scrape_timeline, post_tweet
from build_dictionary import build_new_dict
from markov import generate_models

# -----------------------------------------------------------------------------


def main():
    '''
    Usage: ./main.py [username] [-n]
    if first time running for particular user, [-n] to create new dict/model

    before use, input user credentials in get_tweets.py
    '''
    parser = argparse.ArgumentParser(
        description='Generates haikus from user timeline data'
        ' via. Markov chains')
    parser.add_argument(
        'user', help='User data to generate model from', type=str)
    parser.add_argument('-n', '--new_user', help='Create new dict for new user',
                        action='store_true')
    args = parser.parse_args()

    if args.new_user:
        if not os.path.exists(args.user):
            os.makedirs(args.user)
        os.chdir(args.user)

        scrape_timeline(args.user, 50)
        build_new_dict()
    else:
        os.chdir(args.user)

    good_haiku = False
    while not good_haiku:
        haiku = generate_models()
        post = input('Post?\n%s\n' % haiku)
        if post.lower() == 'y':
            post_tweet(haiku, user=args.user)
            cont = input('Continue?\n\n')
            if cont.lower() == 'y':
                continue
            else:
                good_haiku = True


if __name__ == '__main__':
    main()

    # -----------------------------------------------------------------------------
