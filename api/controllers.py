# -*- coding: utf-8 -*-
import json
from django.shortcuts import HttpResponse
from userpanel.models import UserCollection
from django.views.decorators.csrf import csrf_exempt


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
