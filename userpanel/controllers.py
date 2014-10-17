__author__ = 'bardia'

from django.shortcuts import HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from userpanel.models import UserCollection


@login_required(login_url='/authentication/login/')
def changeDays(request):
    user_id = request.user.id
    us = UserCollection.objects(user_id=user_id)
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
def changeFoodOrder(request):
    us = UserCollection.objects(user_id=request.user.id)
    if len(us) != 1:
        return HttpResponse("not active")
    user = us[0]
    l1 = [int(food_id) for food_id in request.POST.get("food_list_1", "").split()]
    l2 = [int(food_id) for food_id in request.POST.get("food_list_2", "").split()]
    l3 = [int(food_id) for food_id in request.POST.get("food_list_3", "").split()]

    # TODO: check ids

    user.food_list_1 = l1
    user.food_list_2 = l2
    user.food_list_3 = l3
    user.save()
    return HttpResponse("changed")


@login_required(login_url='/authentication/login/')
def changeEmail(request):
    request.user.email = request.POST.get("new_email")
    request.user.save()
    return HttpResponse("changed")


