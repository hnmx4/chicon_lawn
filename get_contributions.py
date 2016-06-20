# -*- coding:utf-8 -*-

import sys
import json
import urllib2
from bs4 import BeautifulSoup

level = {
  '#eeeeee': 0,
  '#d6e685': 1,
  '#8cc665': 2,
  '#44a340': 3,
  '#1e6823': 4
}

def pick_dayly_count(username):
  url = 'https://github.com/users/' + username + '/contributions'
  res = urllib2.urlopen(urllib2.Request(url))
  data = {}
  html = res.read()
  soup = BeautifulSoup(html, 'html.parser')
  for rect in soup.find_all('rect'):
    data[rect['data-date']] = level[rect['fill']]
  return data
