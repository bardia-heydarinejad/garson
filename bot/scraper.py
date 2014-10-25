# -*- coding: utf-8 -*-
import http.cookiejar
import urllib
from bs4 import BeautifulSoup
import re
import datetime
from bot.jalali import JalaliToGregorian

__author__ = 'bardia'

url = "https://stu.iust.ac.ir/loginpage.rose"


def check(username, password):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    authentication_url = "https://stu.iust.ac.ir/j_security_check"
    payload = {"j_username": username,
               "j_password": password,
               "login": u"ورود", }
    data = urllib.parse.urlencode(payload)
    binary_data = data.encode('UTF-8')
    req = urllib.request.Request(authentication_url, binary_data)
    resp = urllib.request.urlopen(req)
    contents = str(resp.read(), 'utf-8')

    if 'iconWarning.gif' in contents:
        # print contents
        return False, None, None

    soup = BeautifulSoup(contents)
    user_info = soup.body.table.tr.find_all('td')[4].div.contents[0]
    user_info = user_info.replace(u'\xA0', ' ').replace('\n', " ")
    matches = re.findall(r"\d{8}", user_info)
    if len(matches) != 1:
        return False, None, None
    uni_id = matches[0]
    name = user_info.replace(uni_id, "").strip()
    if len(name) < 3:
        return False, None, None
    return [True, name, uni_id]


def credit(username, password):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    authentication_url = "https://stu.iust.ac.ir/j_security_check"
    payload = {"j_username": username,
               "j_password": password,
               "login": u"ورود", }
    data = urllib.parse.urlencode(payload)
    binary_data = data.encode('UTF-8')
    req = urllib.request.Request(authentication_url, binary_data)
    resp = urllib.request.urlopen(req)
    contents = str(resp.read())

    if 'iconWarning.gif' in contents:
        print("error")
        return False

    credit_url = "https://stu.iust.ac.ir/nurture/user/multi/reserve/showPanel.rose"

    req = urllib.request.Request(credit_url, binary_data)
    resp = urllib.request.urlopen(req)
    contents = resp.read()
    soup = BeautifulSoup(contents)
    user_credit = soup.find(id="creditId").contents[0]
    # print 'credit:', user_credit
    return int(user_credit)


def today_food(username, password):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    authentication_url = "https://stu.iust.ac.ir/j_security_check"
    payload = {"j_username": username,
               "j_password": password,
               "login": u"ورود", }
    data = urllib.parse.urlencode(payload)
    binary_data = data.encode('UTF-8')
    req = urllib.request.Request(authentication_url, binary_data)
    resp = urllib.request.urlopen(req)
    contents = str(resp.read(), 'utf-8')

    if u'iconWarning.gif' in contents:
        print("error")
        return False

    credit_url = "https://stu.iust.ac.ir/nurture/user/multi/reserve/showPanel.rose"

    req = urllib.request.Request(credit_url, binary_data)
    resp = urllib.request.urlopen(req)
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
    #print(today_food("92521114", "0017578167"))
    #print(credit("92521114", "0017578167"))
    print(check("92521114", "0017578167")[1])
