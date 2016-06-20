# -*- coding:utf-8 -*-

import tweepy
import dotenv
import datetime
from os.path import join, dirname, abspath

import get_contributions as gc


def denv(envkey):
    return dotenv.get_key(join(dirname(__file__), '.env'), envkey)

auth = tweepy.OAuthHandler(denv('CONSUMER_KEY'), denv('CONSUMER_SECRET'))
auth.set_access_token(denv('ACCESS_TOKEN'), denv('ACCESS_SECRET'))
api = tweepy.API(auth)
c = gc.pick_dayly_count(denv('USER'))
yday = datetime.date.today() - datetime.timedelta(1)
yday = yday.strftime('%Y-%m-%d')
yc = str(c[yday])

api.update_profile_image(abspath(dirname(__file__)) + '/' + yc + '.png')
