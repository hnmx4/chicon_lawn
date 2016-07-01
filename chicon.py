# -*- coding:utf-8 -*-

import tweepy
import dotenv
import datetime
import calendar

from bs4 import BeautifulSoup
from os.path import join, dirname, abspath, devnull
from selenium import webdriver


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
    driver = webdriver.PhantomJS(service_log_path=devnull)

    if pform == 'github':
        url = 'https://github.com/users/' + str(username) + '/contributions'
    elif pform == 'gitlab':
        url_login = 'https://gitlab.com/users/sign_in'
        driver.get(url_login)

        loginid = driver.find_element_by_xpath('//input[@name="user[login]"]')
        passwd = driver.find_element_by_xpath('//input[@name="user[password]"]')
        loginid.send_keys(denv('USER_GITLAB'))
        passwd.send_keys(denv('PASSWD_GITLAB'))

        driver.find_element_by_name('commit').submit()

        url = 'https://gitlab.com/u/' + str(username)

    driver.get(url)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    return soup


def pick_dayly_level(username_hub, username_lab):
    soup_hub = get_soup('github', username_hub)
    soup_lab = get_soup('gitlab', username_lab)

    data = {}
    for rect in soup_hub.find_all('rect'):
        data[rect['data-date']] = LEVEL_HUB[rect['fill']]

    months = {}
    for i, v in enumerate(calendar.month_abbr):
        months[v] = i
    for rect in soup_lab.find_all('rect', attrs={'class': 'user-contrib-cell'}):
        src = rect['data-original-title']
        date = src.split('>')[1]
        date = date.split()
        date = (
            str(date[2]) + '-' +
            '{0:0>2}'.format(str(months[date[0]])) + '-' +
            '{0:0>2}'.format(str(date[1]).rstrip(','))
        )
        if date in data:
            data[date] += LEVEL_LAB[rect['fill']]
        else:
            data[rect[date]] = LEVEL_LAB[rect['fill']]

    return data


auth = tweepy.OAuthHandler(denv('CONSUMER_KEY'), denv('CONSUMER_SECRET'))
auth.set_access_token(denv('ACCESS_TOKEN'), denv('ACCESS_SECRET'))
api = tweepy.API(auth)

lv = pick_dayly_level(denv('USER_GITHUB'), denv('USER_GITLAB'))
yday = datetime.date.today() - datetime.timedelta(1)
yday = yday.strftime('%Y-%m-%d')

api.update_profile_image(
    abspath(dirname(__file__)) + '/icons/' +
    (lambda x: 'ex' if x > 4 else str(x))(lv[yday]) + '.png'
)
