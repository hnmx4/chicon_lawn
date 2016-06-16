# -*- coding:utf-8 -*-

import sys
import json
import urllib2
from bs4 import BeautifulSoup


def pick_count_list(url):
  res = urllib2.urlopen(urllib2.Request(url))
  lists = []
  html = res.read()
  soup = BeautifulSoup(html, 'html.parser')
  for rect in soup.find_all('rect'):
    lists.append(rect['data-count'])
  return lists
