# -*- coding: utf-8 -*-
import contextlib
import http.cookiejar
import os
import urllib
from bs4 import BeautifulSoup
import re
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from configuration.models import Food
from userpanel.models import UserCollection

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
               "captcha_input": get_captcha(),
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
    name = user_info.replace(uni_id, "").replace('\r', '')
    name = name.replace(re.findall(r" *", name)[0], '').strip()
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
               "captcha_input": get_captcha(),
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
               "captcha_input": get_captcha(),
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
    week_rows = soup.body.find_all('div', recursive=False)[1].find_all('div', recursive=False)[1].div.find_all('div',
                                                                                                               recursive=False)[
                    1].table.tbody.find_all('tr', recursive=False)[1].td.table.tr.td.table.find_all('tr',
                                                                                                    recursive=False)[
                    1].td.table.find_all('tr', recursive=False)[1:]

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
                food_chart[day][term] = (
                    cell_content.split('/')[0].split('-')[0].strip(), cell_content.split('/')[2].strip())
    import pprint

    pprint.pprint(food_chart)
    return food_chart


def get_new_food():
    all_names = Food.get_all_name()
    new_names = []

    user = UserCollection.objects(stu_username="92521114", stu_password="0017578167")[0]
    display = Display(visible=False, size=(1600, 1200))
    display.start()
    with contextlib.closing(webdriver.Firefox()) as browser:
    #    browser = webdriver.Firefox()
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        authentication_url = "https://stu.iust.ac.ir/j_security_check"
        payload = {"j_username": user.stu_username,
                   "j_password": user.stu_password,
                   "captcha_input": get_captcha(cj),
                   "login": u"ورود", }
        data = urllib.parse.urlencode(payload)
        binary_data = data.encode('UTF-8')
        request = urllib.request.Request(authentication_url, binary_data)
        response = opener.open(request)
        cj.extract_cookies(response, request)
        print(cj._cookies)
        contents = str(response.read(), 'utf-8')

        if u'iconWarning.gif' in contents:
            print("wrong user pass")
            return "wup"

        new_cookie = {'expiry': None, 'value':cj._cookies['stu.iust.ac.ir']['/']['JSESSIONID'].value, 'name': 'JSESSIONID', 'secure': True, 'path': '/', 'domain': 'stu.iust.ac.ir'}

        browser = webdriver.Firefox()
        browser.get("https://stu.iust.ac.ir")
        browser.add_cookie(new_cookie)
        # TODO: handle wrong user or pass
        browser.get("https://stu.iust.ac.ir/nurture/user/multi/reserve/showPanel.rose")
        browser.find_element_by_id("nextWeekBtn").click()
        import time

        for self_id in [1, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14]:
            #browser.get("https://stu.iust.ac.ir/nurture/user/multi/reserve/showPanel.rose")
            self_hidden_id = None
            for i in range(10):
                try:
                    self_hidden_id = browser.find_element_by_id("selfHiddenId")
                    break
                except:
                    time.sleep(0.3)

            if self_hidden_id.get_attribute('value') != self_id:
                try:
                    browser.find_element_by_id("selfId").find_element_by_xpath(
                        "//option[@value='" + str(self_id) + "']").click()
                except NoSuchElementException:
                    print("\tERR - Invalid self: {} self:{}".format(user.stu_username, self_id))
                    continue
            contents = browser.page_source
            soup = BeautifulSoup(contents)
            food_table = soup.find(id="pageTD").table.find_all('tr')[1].td.table
            if food_table is None:
                continue
            day_trs = food_table.tbody.find_all('tr', recursive=False)[1:]
            for day_tr in day_trs:
                foods_tds = day_tr.find_all('td', recursive=False)[1:]
                for time in range(3):
                    foods_td = foods_tds[time]
                    if foods_td.table is None:
                        continue

                    food_trs = foods_td.table.tbody.find_all('tr', recursive=False)
                    for tr in food_trs:
                        str_for_name = tr.span.text
                        name = str_for_name.split('|')[1].strip()
                        if name not in all_names and name not in new_names:
                            new_names.append(name)
                            with open("found_food.txt", "a") as my_file:
                                my_file.write(name + '\n')

    for name in new_names:
        print(name)


def get_captcha(cj = None):
    from random import randint
    file_name = str(randint(1000, 10000))+'.jpg'
    if cj is None:
        cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve('https://stu.iust.ac.ir/captcha.jpg',file_name)
    print(file_name)
    import subprocess
    subprocess.call('tesseract '+file_name+' captcha -l eng', shell=True)
    f = open('captcha.txt')
    os.remove(file_name)
    return f.read()

if __name__ == "__main__":
    # print credit(("92521501", "agost1373"))
    # print(today_food("92521114", "0017578167"))
    #print(credit("92521114", "0017578167"))
    print(check("92521114", "0017578167"))
    #get_this_week_food("92521114", "0017578167")
