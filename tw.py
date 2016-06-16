# -*- coding:utf-8 -*-

import tweepy
import dotenv
from os.path import join, dirname

import get_contributions as gc


def denv(envkey):
    return dotenv.get_key(join(dirname(__file__), '.env'), envkey)

auth = tweepy.OAuthHandler(denv('CONSUMER_KEY'), denv('CONSUMER_SECRET'))
auth.set_access_token(denv('ACCESS_TOKEN'), denv('ACCESS_SECRET'))
api = tweepy.API(auth)

url = 'https://github.com/users/' + denv('USER') + '/contributions'
lists = gc.pick_count_list(url)
nc = int(lists[-1])
select = lambda c: '4' if c > 4 else str(c)

api.update_profile_image(select(nc)+'.png')
