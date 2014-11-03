# -*- coding: utf-8 -*-
import http.cookiejar
import urllib
from bs4 import BeautifulSoup
import re
#import datetime
#from bot.jalali import JalaliToGregorian

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
    #print(contents)

    if 'iconWarning.gif' in contents:
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


def get_this_week_food(username, password):
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

    food_url = "https://stu.iust.ac.ir/nurture/user/multi/reserve/displayPanel.rose"

    req = urllib.request.Request(food_url, binary_data)
    resp = urllib.request.urlopen(req)
    contents = resp.read()
    soup = BeautifulSoup(contents)

    food_chart = [[None, None, None] for i in range(6)]
    # /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody
    week_rows = soup.body.find_all('div', recursive=False)[1].find_all('div', recursive=False)[1].div.find_all('div', recursive=False)[1].table.tbody.find_all('tr', recursive=False)[1].td.table.tr.td.table.find_all('tr', recursive=False)[1].td.table.find_all('tr', recursive=False)[1:]

    for day_tr in week_rows:
        day = 6
        if str(day_tr).find(u"پنجشنبه") != -1:
            day = 5
        elif str(day_tr).find(u"چهارشنبه") != -1:
            day = 4
        elif str(day_tr).find(u"سه شنبه") != -1:
            day = 3
        elif str(day_tr).find(u"دوشنبه") != -1:
            day = 2
        elif str(day_tr).find(u"یکشنبه") != -1:
            day = 1
        elif str(day_tr).find(u"شنبه") != -1:
            day = 0

        for term, food_cell in enumerate(day_tr.find_all('td', recursive=False)[1:]):
            cell_content = food_cell.text.strip()
            if cell_content != "":
                food_chart[day][term] = (cell_content.split('/')[0].split('-')[0].strip(), cell_content.split('/')[2].strip())
    import pprint
    pprint.pprint(food_chart)
    return food_chart


if __name__ == "__main__":
    # print credit(("92521501", "agost1373"))
    # print(today_food("92521114", "0017578167"))
    #print(credit("92521114", "0017578167"))
    print(check("92521114", "0017578167"))
    #get_this_week_food("92521114", "0017578167")
