# -*- coding: utf-8 -*-
import random
from bs4 import BeautifulSoup
import re
from configuration.models import Food
from userpanel.models import UserCollection
from selenium import webdriver
from pyvirtualdisplay import Display
import contextlib


__author__ = 'bardia'


def _get_foods(contents):
    all_names = Food.get_all_name()

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
                if name not in all_names:
                    with open("found_food.txt", "a") as my_file:
                        my_file.write(name + '\n')

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

    def register(self):
        try:
            display = Display(visible=False, size=(1600, 1200))
            display.start()
            with contextlib.closing(webdriver.Firefox()) as browser:
                #browser = webdriver.Firefox()
                browser.get("https://stu.iust.ac.ir")
                browser.find_element_by_id("j_username").send_keys(self.user.stu_username)
                browser.find_element_by_id("j_password").send_keys(self.user.stu_password)
                browser.find_element_by_id("login_btn_submit").submit()
                # TODO: handle wrong user or pass
                browser.get("https://stu.iust.ac.ir/nurture/user/multi/reserve/showPanel.rose")
                browser.find_element_by_id("nextWeekBtn").click()

                for self_id in set(self.user.breakfast + self.user.lunch + self.user.dinner) - {0}:
                    #browser.get("https://stu.iust.ac.ir/nurture/user/multi/reserve/showPanel.rose")
                    if browser.find_element_by_id("selfHiddenId").get_attribute('value') != self_id:
                        browser.find_element_by_id("selfId").find_element_by_xpath(
                            "//option[@value='" + str(self_id) + "']").click()
                    foods_to_register = []
                    food_chart = _get_foods(browser.page_source)

                    for i, day in enumerate(self.user.breakfast):
                        if day == self_id:
                            foods_in_day = food_chart[i][0]
                            if len(foods_in_day) > 0:
                                foods_to_register += [choose_food(self.user, foods_in_day)]
                    for i, day in enumerate(self.user.lunch):
                        if day == self_id:
                            foods_in_day = food_chart[i][1]
                            if len(foods_in_day) > 0:
                                foods_to_register += [choose_food(self.user, foods_in_day)]
                    for i, day in enumerate(self.user.dinner):
                        if day == self_id:
                            foods_in_day = food_chart[i][2]
                            if len(foods_in_day) > 0:
                                foods_to_register += [choose_food(self.user, foods_in_day)]

                    for index, food_to_check in foods_to_register:
                        browser.find_element_by_id("userWeekReserves.selected" + str(index)).click()
                    browser.find_element_by_id("doReservBtn").click()

        except Exception as e:
            return str(e)
            browser.quit()
        # display.stop()
        return None


if __name__ == "__main__":
    # user = UserCollection.objects(stu_username="92522267", stu_password="0440518075")[0]
    user = UserCollection.objects(stu_username="92521114", stu_password="0017578167")[0]
    reg = Registerer(user)
    reg.register()
    # # print(choose_food(user, [('6', 'رشته پلو'), ('7', 'زرشك پلو با مرغ')]))
