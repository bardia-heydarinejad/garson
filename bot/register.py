# -*- coding: utf-8 -*-
import pprint
import random
import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import re
from bot.scraper import encoded_dict
from configuration.models import Food

from userpanel.models import UserCollection

__author__ = 'bardia'


def _get_foods(contents):
    food_chart = [[[], [], []] for i in range(6)]
    # for day in range(5):
    # for time in range(3):
    # food_chart[day][time] = 1
    soup = BeautifulSoup(contents)
    day_trs = soup.find(id="pageTD").table.find_all('tr')[1].td.table.find_all('tr', recursive=False)[1:]
    for day_tr in day_trs:
        if unicode(day_tr).find(u"پنجشنبه") != -1:
            day = 5
        elif unicode(day_tr).find(u"چهارشنبه") != -1:
            day = 4
        elif unicode(day_tr).find(u"سه شنبه") != -1:
            day = 3
        elif unicode(day_tr).find(u"دوشنبه") != -1:
            day = 2
        elif unicode(day_tr).find(u"یکشنبه") != -1:
            day = 1
        elif unicode(day_tr).find(u"شنبه") != -1:
            day = 0
        foods_tds = day_tr.find_all('td', recursive=False)[1:]
        for time in range(3):
            foods_td = foods_tds[time]
            if foods_td.table is None:
                continue

            food_trs = foods_td.table.find_all('tr', recursive=False)
            for tr in food_trs:
                number = re.findall(r'id="userWeekReserves\.selected(\d+)"', str(tr))[0]
                name = re.findall(r'\|(.+)\|', str(tr))[0].strip()
                food_chart[day][time].append((number, name))

    # from pprint import pprint
    # pprint(food_chart)
    return food_chart


def _init_data(contents, foods):
    soup = BeautifulSoup(contents)
    data = {}
    for input_tag in soup.find_all("form")[0].find_all("input"):
        if input_tag.has_attr('name'):
            if input_tag.has_attr('value'):
                data[input_tag['name']] = input_tag['value']
            else:
                data[input_tag['name']] = ""
    pprint.pprint(data)
    return encoded_dict(data)


def choose_food(user, foods):
    random_choice = []

    list1 = [Food.get_name(i) for i in user.food_list_1]
    list2 = [Food.get_name(i) for i in user.food_list_2]

    for fav_food in list1:
        for food in foods:
            if food[1] == fav_food:
                return food
    for food in foods:
        if food[1] in list2:
            random_choice.append(food)
    if len(random_choice) > 0:
        return random.choice(random_choice)
    return None, None


def register(user):
    # Store the cookies and create an opener that will hold them
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    # Add our headers
    opener.addheaders = [('User-agent', 'RedditTesting')]

    # Install our opener (note that this changes the global opener to the one
    # we just made, but you can also just call opener.open() if you want)
    urllib2.install_opener(opener)

    # The action/ target from the form
    authentication_url = "https://stu.iust.ac.ir/j_security_check"

    # Input parameters we are going to send
    payload = encoded_dict({"j_username": user.stu_username,
                            "j_password": user.stu_password,
                            "login": u"ورود", })

    # Use urllib to encode the payload
    data = urllib.urlencode(payload)

    # Build our Request object (supplying 'data' makes it a POST)
    req = urllib2.Request(authentication_url, data)

    # Make the request and read the response
    resp = urllib2.urlopen(req)
    contents = resp.read()

    if contents.find('iconWarning.gif') != -1:
        print "error"
        return False
    #

    register_url = "https://stu.iust.ac.ir/nurture/user/multi/reserve/showPanel.rose"

    req = urllib2.Request(register_url, data)

    # Make the request and read the response
    resp = urllib2.urlopen(req)
    contents = resp.read()

    chart = _get_foods(contents)
    food_to_register = []
    for day in chart:
        print "Day"
        for time in day:
            print "\tTime"
            print '\t Chosen:', choose_food(user, time)
            food_to_register.append(choose_food(user, time))

    data = _init_data(contents, food_to_register)

    req = urllib2.Request(register_url, data)
    resp = urllib2.urlopen(req)
    contents = resp.read()

if __name__ == "__main__":
    print register(("92521114", "0017578167"))