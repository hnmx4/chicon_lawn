# -*- coding:utf-8 -*-

import tweepy
import dotenv
import datetime
import urllib2
import calendar

from bs4 import BeautifulSoup
from os.path import join, dirname, abspath


LEVEL_HUB = {
    '#eeeeee': 0,
    '#d6e685': 1,
    '#8cc665': 2,
    '#44a340': 3,
    '#1e6823': 4
}

LEVEL_LAB = {
    '#ededed': 0,
    '#acd5f2': 1,
    '#7fa8c9': 2,
    '#527ba0': 3,
    '#254e77': 4
}


def denv(envkey):
    return dotenv.get_key(join(dirname(__file__), '.env'), envkey)


def get_soup(pform, username):
    if pform == 'github':
        url = 'https://github.com/users/' + username + '/contributions'
    elif pform == 'gitlab':
        url = 'https://gitlab.com/u/' + username

    res = urllib2.urlopen(urllib2.Request(url))
    html = res.read()
    soup = BeautifulSoup(html, 'html.parser')

    return soup


def pick_dayly_level(username_hub, username_lab):
    soup_hub = get_soup('github', username_hub)
    soup_lab = get_soup('gitlab', username_lab)

    data = {}
    for rect in soup_hub.find_all('rect'):
        data[rect['data-date']] = LEVEL_HUB[rect['fill']]

    return data


auth = tweepy.OAuthHandler(denv('CONSUMER_KEY'), denv('CONSUMER_SECRET'))
auth.set_access_token(denv('ACCESS_TOKEN'), denv('ACCESS_SECRET'))
api = tweepy.API(auth)

lv = pick_dayly_level(denv('USER_GITHUB'), denv('USER_GITLAB'))
yday = datetime.date.today() - datetime.timedelta(1)
yday = yday.strftime('%Y-%m-%d')

api.update_profile_image(abspath(dirname(__file__)) + '/' + str(lv[yday]) + '.png')
