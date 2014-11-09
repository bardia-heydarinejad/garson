# -*- coding: utf-8 -*-
import json
from django.shortcuts import HttpResponse
from userpanel.models import UserCollection
from django.views.decorators.csrf import csrf_exempt
from api.model import CookieCollection


@csrf_exempt
def user_credit(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    res = UserCollection.objects(stu_username=username, stu_password=password)
    if len(res) > 0:
        user = res[0]
        return HttpResponse(user.credit)
    return HttpResponse("wrong_user_pass")


@csrf_exempt
def this_week_foods(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    print(username, password)
    res = UserCollection.objects(stu_username=username, stu_password=password)
    if len(res) > 0:
        user = res[0]
        chart = user.reserved_food
        return HttpResponse(json.dumps(chart))
    return HttpResponse("wrong_user_pass")


import datetime

@csrf_exempt
def set_cookie(request):
    cookie = request.GET.get("MoodleSession")
    if len(CookieCollection.objects(cookie=cookie)) == 0:
        cc = CookieCollection()
        cc.cookie = cookie
        cc.time = datetime.datetime.now()
        cc.save()
        return HttpResponse("ok")
    return HttpResponse("nok")


def get_cookie(request):
    s = ""
    for cookie in CookieCollection.objects():
        if cookie.time is None or cookie.time + datetime.timedelta(minutes=30) < datetime.datetime.now():
            cookie.delete()
        else:
            s += cookie.cookie + '/'
    return HttpResponse(s)


def del_cookie(request):
    cookie = request.GET.get("MoodleSession")
    if len(CookieCollection.objects(cookie=cookie)) != 0:
        CookieCollection.objects(cookie=cookie)[0].delete()
    return HttpResponse("")
