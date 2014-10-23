# -*- coding: utf-8 -*-
from jalali import JalaliToGregorian

__author__ = 'bardia'

url = "https://stu.iust.ac.ir/loginpage.rose"
import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import re
import datetime


def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict


def check((username, password)):
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
        # print contents
        return False, None, None

    soup = BeautifulSoup(contents)
    user_info = soup.body.table.tr.find_all('td')[4].div.contents[0]
    user_info = user_info.replace(u'\xA0', ' ').replace('\n', " ").decode().encode('utf8')
    matches = re.findall(r"\d{8}", user_info)
    if len(matches) != 1:
        return False, None, None
    uni_id = matches[0]
    name = unicode(user_info).replace(uni_id, "").strip()
    if len(name) < 3:
        return False, None, None
    return True, name, uni_id


def credit((username, password)):
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

    credit_url = "https://stu.iust.ac.ir/nurture/user/multi/reserve/showPanel.rose"

    req = urllib2.Request(credit_url, data)

    # Make the request and read the response
    resp = urllib2.urlopen(req)
    contents = resp.read()
    soup = BeautifulSoup(contents)
    user_credit = soup.find(id="creditId").contents[0]
    # print 'credit:', user_credit
    return int(user_credit)


def today_food((username, password)):
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

    credit_url = "https://stu.iust.ac.ir/nurture/user/multi/reserve/showPanel.rose"

    req = urllib2.Request(credit_url, data)

    # Make the request and read the response
    resp = urllib2.urlopen(req)
    contents = resp.read()
    soup = BeautifulSoup(contents)

    food_rows = soup.find(id="pageTD").table.find_all('tr')[1].td.table.find_all('tr', recursive=False)[1:]

    for food_row in food_rows:
        j_date = (re.findall(r"\d{4}\/\d{2}\/\d{2}", str(food_row))[0]).split('/')

        g_date = JalaliToGregorian(int(j_date[0]), int(j_date[1]), int(j_date[2])).getGregorianList()

        datetime_now = datetime.datetime.now()
        c_g_date = (datetime_now.year, datetime_now.month, datetime_now.day)
        if c_g_date == g_date:
            for food_input in food_row.find_all("input"):
                if food_input.has_attr("checked"):
                    number = re.findall(r'id="userWeekReserves\.selected(\d+)"', str(food_input))[0]
                    span_id = "foodNameSpan" + number
                    span = food_row.find_all("span", attrs={'id': span_id})[0]
                    return re.findall(r'\|(.+)\|', str(span))[0].strip()
    return '-'


if __name__ == "__main__":
    # print credit(("92521501", "agost1373"))
    print today_food(("92521114", "0017578167"))
    # print credit(("92521114", "0017578167"))
    # print check(("92521114", "0017578167"))