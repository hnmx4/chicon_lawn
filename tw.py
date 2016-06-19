# -*- coding:utf-8 -*-

import tweepy
import dotenv
import datetime
from os.path import join, dirname

import get_contributions as gc


def denv(envkey):
    return dotenv.get_key(join(dirname(__file__), '.env'), envkey)

auth = tweepy.OAuthHandler(denv('CONSUMER_KEY'), denv('CONSUMER_SECRET'))
auth.set_access_token(denv('ACCESS_TOKEN'), denv('ACCESS_SECRET'))
api = tweepy.API(auth)
url = 'https://github.com/users/' + denv('USER') + '/contributions'
c = gc.pick_dayly_count(url)
yday = datetime.date.today() - datetime.timedelta(1)
yday = yday.strftime('%Y-%m-%d')
yc = int(c[yday])

select = lambda c: '4' if c > 4 else str(c)

api.update_profile_image(select(yc) + '.png')
