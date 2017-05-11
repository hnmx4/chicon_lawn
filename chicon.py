# -*- coding:utf-8 -*-
import tweepy
import dotenv
import datetime
import calendar

from bs4 import BeautifulSoup
from os import path
from selenium import webdriver


LEVEL_HUB = {
    '#ebedf0': 0,
    '#c6e48b': 1,
    '#7bc96f': 2,
    '#239a3b': 3,
    '#196127': 4
}
LEVEL_LAB = {
    '#ededed': 0,
    '#acd5f2': 1,
    '#7fa8c9': 2,
    '#527ba0': 3,
    '#254e77': 4
}


def denv(envkey):
    return dotenv.get_key(path.join(path.dirname(__file__), '.env'), envkey)


def get_soup(pform, username):
    driver = webdriver.PhantomJS(service_log_path=path.devnull)

    if pform == 'github':
        url = 'https://github.com/users/' + str(username) + '/contributions'
    elif pform == 'gitlab':
        url_login = 'https://gitlab.com/users/sign_in'
        driver.get(url_login)
        loginid = driver.find_element_by_xpath('//input[@id="user_login"]')
        passwd = driver.find_element_by_xpath('//input[@id="user_password"]')
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
    # soup_lab = get_soup('gitlab', username_lab)

    data = {}
    for rect in soup_hub.find_all('rect'):
        data[rect['data-date']] = LEVEL_HUB[rect['fill']]

    months = {}
    for i, v in enumerate(calendar.month_abbr):
        months[v] = i
    # for rect in soup_lab.find_all('rect',
    #                               attrs={'class': 'user-contrib-cell'}):
    #     src = rect['data-original-title'].split('>')[1].split()
    #     date = '-'.join([
    #         str(src[3]),
    #         '{0:0>2}'.format(str(months[src[1]])),
    #         '{0:0>2}'.format(str(src[2]).rstrip(','))
    #     ])
    #     if date in data:
    #         data[date] += LEVEL_LAB[rect['fill']]
    #     else:
    #         data[date] = LEVEL_LAB[rect['fill']]

    return data


lv = pick_dayly_level(denv('USER_GITHUB'), denv('USER_GITLAB'))
yday = datetime.date.today() - datetime.timedelta(1)
yday = yday.strftime('%Y-%m-%d')

auth = tweepy.OAuthHandler(denv('CONSUMER_KEY'), denv('CONSUMER_SECRET'))
auth.set_access_token(denv('ACCESS_TOKEN'), denv('ACCESS_SECRET'))
api = tweepy.API(auth)

print('-----' + str(datetime.datetime.today()) + '-----')
api.update_profile_image(
    path.join(path.abspath(path.dirname(__file__)),
              'icons',
              (lambda x: 'ex' if x > 4 else str(x))(lv[yday]) + '.png')
)
