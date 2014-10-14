__author__ = 'bardia'

from django.shortcuts import HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from userpanel.models import UserCollection


@login_required(login_url='/authentication/login/')
def changeDays(request):
    user_id = request.user.id
    us = UserCollection.objects(userId=user_id)
    if len(us) != 1:
        return HttpResponse("not active")
    user = us[0]

    user.sat = int(request.POST.get("sat", "0")) if request.POST.get("sat", "0") != "" else "0"
    user.sun = int(request.POST.get("sun", "0")) if request.POST.get("sun", "0") != "" else "0"
    user.mon = int(request.POST.get("mon", "0")) if request.POST.get("mon", "0") != "" else "0"
    user.tue = int(request.POST.get("tue", "0")) if request.POST.get("tue", "0") != "" else "0"
    user.wed = int(request.POST.get("wed", "0")) if request.POST.get("wed", "0") != "" else "0"
    user.thu = int(request.POST.get("thu", "0")) if request.POST.get("thu", "0") != "" else "0"
    user.fri = int(request.POST.get("fri", "0")) if request.POST.get("fri", "0") != "" else "0"

    user.save()

    return HttpResponse("changed")


@login_required(login_url='/authentication/login/')
def changeName(request):
    user_id = request.user.id
    us = UserCollection.objects(userId=user_id)
    if len(us) != 1:
        return HttpResponse("not active")
    user = us[0]
    name = request.POST.get("name", "")
    if not 3 < len(name) < 75:
        return HttpResponse("invalid name")

    uni_id = request.POST.get("uni_id", "")
    if len(uni_id) != 8:
        return HttpResponse("invalid uni id")

    user.uni_id = uni_id
    user.name = name
    user.save()

    return HttpResponse("changed")


@login_required(login_url='/authentication/login/')
def changeFoodOrder(request):
    us = UserCollection.objects(userId=request.user.id)
    if len(us) != 1:
        return HttpResponse("not active")
    user = us[0]
    l = [int(food_id) for food_id in request.POST.get("list", "").split()]
    user.favorites = l
    user.save()
    return HttpResponse("changed")


@login_required(login_url='/authentication/login/')
def changeBanFood(request):
    us = UserCollection.objects(userId=request.user.id)
    if len(us) != 1:
        return HttpResponse("not active")
    user = us[0]
    l = [int(food_id) for food_id in request.POST.get("list", "").split()]
    user.favorites = l
    user.save()
    return HttpResponse("changed")


@login_required(login_url='/authentication/login/')
def changeStu(request):
    us = UserCollection.objects(userId=request.user.id)
    if len(us) != 1:
        return HttpResponse("not active")
    user = us[0]
    if request.POST.get("username", "") != "":
        user.stu_username = request.POST.get("username")
    if request.POST.get("password", "") != "":
        user.stu_password = request.POST.get("password")
    user.save()
    return HttpResponse("changed")

