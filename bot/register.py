# -*- coding: utf-8 -*-
import pprint
import random
from bs4 import BeautifulSoup
import re
from configuration.models import Food

from userpanel.models import UserCollection
from selenium import webdriver


__author__ = 'bardia'


def _get_foods(contents):
    food_chart = [[[], [], []] for i in range(6)]
    soup = BeautifulSoup(contents)
    day_trs = soup.find(id="pageTD").table.find_all('tr')[1].td.table.tbody.find_all('tr', recursive=False)[1:]
    for day_tr in day_trs:
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
        else:
            print('error')
            continue
        foods_tds = day_tr.find_all('td', recursive=False)[1:]
        for time in range(3):
            foods_td = foods_tds[time]
            if foods_td.table is None:
                continue

            food_trs = foods_td.table.tbody.find_all('tr', recursive=False)
            for tr in food_trs:
                number = re.findall(r'id="userWeekReserves\.selected(\d+)"', str(tr))[0]
                name = re.findall(r'\|(.+)\|', str(tr))[0].strip()
                food_chart[day][time].append((number, name))

    return food_chart


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


class Registerer:
    food_chart = None

    def __init__(self, user):
        self.user = user
        self.browser = webdriver.Firefox()

    def register(self):
        self.browser.get("https://stu.iust.ac.ir")
        self.browser.find_element_by_id("j_username").send_keys(self.user.stu_username)
        self.browser.find_element_by_id("j_password").send_keys(self.user.stu_password)
        self.browser.find_element_by_id("login_btn_submit").submit()
        # TODO: handle wrong user or pass
        # if contents.find('iconWarning.gif') != -1:
        # print "error"
        self.browser.get("https://stu.iust.ac.ir/nurture/user/multi/reserve/showPanel.rose")
        self.browser.find_element_by_id("nextWeekBtn").click()

        if Registerer.food_chart is None:
            Registerer.food_chart = _get_foods(self.browser.page_source)

        food_to_register = {}
        for i, day in enumerate(Registerer.food_chart):
            for j, time in enumerate(day):
                if j == 0:
                    self_id = self.user.breakfast[i]
                if j == 1:
                    self_id = self.user.lunch[i]
                if j == 2:
                    self_id = self.user.dinner[i]
                if self_id != 0:
                    if not self_id in food_to_register:
                        food_to_register[self_id] = [choose_food(self.user, time)]
                    else:
                        food_to_register[self_id].append(choose_food(self.user, time))

        food_to_register = food_to_register[1]
        for i, food_name in food_to_register:
            self.browser.find_element_by_id("userWeekReserves.selected"+str(i)).click()
        self.browser.find_element_by_id("doReservBtn").click()
        self.browser.quit()
        return


if __name__ == "__main__":
    reg = Registerer(UserCollection.objects(stu_username="92521114", stu_password="0017578167")[0])
    reg.register()
