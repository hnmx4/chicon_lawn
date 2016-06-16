# -*- coding:utf-8 -*-

import tweepy
import dotenv
from os.path import join, dirname


def denv(envkey):
    return dotenv.get_key(join(dirname(__file__), '.env'), envkey)

auth = tweepy.OAuthHandler(denv('CONSUMER_KEY'), denv('CONSUMER_SECRET'))
auth.set_access_token(denv('ACCESS_TOKEN'), denv('ACCESS_SECRET'))
api = tweepy.API(auth)
