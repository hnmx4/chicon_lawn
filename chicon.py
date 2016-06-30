# -*- coding:utf-8 -*-

import tweepy
import dotenv
import datetime
import urllib2

from bs4 import BeautifulSoup
from os.path import join, dirname, abspath


def denv(envkey):
    return dotenv.get_key(join(dirname(__file__), '.env'), envkey)


def pick_dayly_level(username):
    url = 'https://github.com/users/' + username + '/contributions'
    res = urllib2.urlopen(urllib2.Request(url))
    data = {}
    html = res.read()
    soup = BeautifulSoup(html, 'html.parser')
    level = {
        '#eeeeee': 0,
        '#d6e685': 1,
        '#8cc665': 2,
        '#44a340': 3,
        '#1e6823': 4
    }

    for rect in soup.find_all('rect'):
        data[rect['data-date']] = level[rect['fill']]
    return data


auth = tweepy.OAuthHandler(denv('CONSUMER_KEY'), denv('CONSUMER_SECRET'))
auth.set_access_token(denv('ACCESS_TOKEN'), denv('ACCESS_SECRET'))
api = tweepy.API(auth)

lv = pick_dayly_level(denv('USER'))
yday = datetime.date.today() - datetime.timedelta(1)
yday = yday.strftime('%Y-%m-%d')

api.update_profile_image(abspath(dirname(__file__)) + '/' + str(lv[yday]) + '.png')
