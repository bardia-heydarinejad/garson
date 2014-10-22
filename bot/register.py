# -*- coding: utf-8 -*-
import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import re
import datetime
from bot.scraper import encoded_dict

__author__ = 'bardia'


def _get_foods(contents, day, time):
    foods_list = []
    soup = BeautifulSoup(contents)
    day_tr = soup.find(id="pageTD").table.find_all('tr')[1].td.table.find_all('tr', recursive=False)[day + 1]
    foods_td = day_tr.find_all('td', recursive=False)[time+1]
    if foods_td.table is None:
        return foods_list
    food_trs = foods_td.table.find_all('tr', recursive=False)
    for tr in food_trs:
        number = re.findall(r'id="userWeekReserves\.selected(\d+)"', str(tr))[0]
        name = re.findall(r'\|(.+)\|', str(tr))[0].strip()
        foods_list.append((number,name))
    print foods_list
    return foods_list

def register((username, password)):
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
    payload = encoded_dict({"j_username": username,
                            "j_password": password,
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

    lll = [None,None,None]
    all_foods = [lll]*6
    for day in range(5):
        for time in range(3):
            all_foods[day][time] = _get_foods(contents, day, time)
    return all_foods


if __name__ == "__main__":
    print register(("92521114", "0017578167"))