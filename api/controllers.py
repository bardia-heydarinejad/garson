# -*- coding: utf-8 -*-
import json
from django.shortcuts import HttpResponse
from userpanel.models import UserCollection
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def user_credit(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = UserCollection.objects(stu_username=username, stu_password=password)[0]
    return HttpResponse(user.credit)


@csrf_exempt
def this_week_foods(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = UserCollection.objects(stu_username=username, stu_password=password)[0]
    chart = user.reserved_food
    return HttpResponse(json.dumps(chart))
