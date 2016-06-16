# -*- coding:utf-8 -*-

import sys
import json

from bs4 import BeautifulSoup


def pick_count_week_date_list(res):
  lists = []
  dict_obj = {}
  html = res.read()
  soup = BeautifulSoup(html, 'html.parser')
  for rect in soup.find_all('rect'):
    dict_obj = {
      'data-date'  : rect['data-date'],
      'data-count' : rect['data-count']
      }
    lists.append(dict_obj)
  return lists


def pick_count_list(res):
  lists = []
  html = res.read()
  soup = BeautifulSoup(html, 'html.parser')
  for rect in soup.find_all('rect'):
    lists.append(rect['data-count'])
  return lists
