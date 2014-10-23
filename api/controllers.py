# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import HttpResponse
from bot.scraper import today_food
from userpanel.models import UserCollection
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def today_lunch(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = UserCollection.objects(stu_username=username, stu_password=password)[0]
    today = datetime.datetime.now().date()
    if not today == user.today_meal_last_update.date():
        user.today_lunch = today_food(("92521114", "0017578167"))
        user.today_meal_last_update = today
        user.save()
    return HttpResponse('-/'+user.today_lunch+'/-')


@csrf_exempt
def user_credit(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = UserCollection.objects(stu_username=username, stu_password=password)[0]
    return HttpResponse(user.credit)
