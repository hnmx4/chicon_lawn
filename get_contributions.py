# -*- coding:utf-8 -*-

import sys
import json
import urllib2
from bs4 import BeautifulSoup


def pick_dayly_count(url):
  res = urllib2.urlopen(urllib2.Request(url))
  data = {}
  html = res.read()
  soup = BeautifulSoup(html, 'html.parser')
  for rect in soup.find_all('rect'):
    data[rect['data-date']] = rect['data-count']
  return data
