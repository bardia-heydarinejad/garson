__author__ = 'bardia'

from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from userpanel.models import UserCollection


@login_required(login_url='/')
def change_days(request):
    user_id = request.user.id
    us = UserCollection.objects(user_id=user_id)
    if len(us) != 1:
        return HttpResponse("not active")
    user = us[0]

    user.breakfast = [0, 0, 0, 0, 0, 0]
    user.breakfast[0] = int(request.POST.get("sat_b", "0")) if request.POST.get("sat_b", "0") != "" else 0
    user.breakfast[1] = int(request.POST.get("sun_b", "0")) if request.POST.get("sun_b", "0") != "" else 0
    user.breakfast[2] = int(request.POST.get("mon_b", "0")) if request.POST.get("mon_b", "0") != "" else 0
    user.breakfast[3] = int(request.POST.get("tue_b", "0")) if request.POST.get("tue_b", "0") != "" else 0
    user.breakfast[4] = int(request.POST.get("wed_b", "0")) if request.POST.get("wed_b", "0") != "" else 0
    user.breakfast[5] = int(request.POST.get("thu_b", "0")) if request.POST.get("thu_b", "0") != "" else 0

    user.lunch = [0, 0, 0, 0, 0, 0]
    user.lunch[0] = int(request.POST.get("sat_l", "0")) if request.POST.get("sat_l", "0") != "" else 0
    user.lunch[1] = int(request.POST.get("sun_l", "0")) if request.POST.get("sun_l", "0") != "" else 0
    user.lunch[2] = int(request.POST.get("mon_l", "0")) if request.POST.get("mon_l", "0") != "" else 0
    user.lunch[3] = int(request.POST.get("tue_l", "0")) if request.POST.get("tue_l", "0") != "" else 0
    user.lunch[4] = int(request.POST.get("wed_l", "0")) if request.POST.get("wed_l", "0") != "" else 0
    user.lunch[5] = int(request.POST.get("thu_l", "0")) if request.POST.get("thu_l", "0") != "" else 0

    user.dinner = [0, 0, 0, 0, 0, 0]
    user.dinner[0] = int(request.POST.get("sat_d", "0")) if request.POST.get("sat_d", "0") != "" else 0
    user.dinner[1] = int(request.POST.get("sun_d", "0")) if request.POST.get("sun_d", "0") != "" else 0
    user.dinner[2] = int(request.POST.get("mon_d", "0")) if request.POST.get("mon_d", "0") != "" else 0
    user.dinner[3] = int(request.POST.get("tue_d", "0")) if request.POST.get("tue_d", "0") != "" else 0
    user.dinner[4] = int(request.POST.get("wed_d", "0")) if request.POST.get("wed_d", "0") != "" else 0
    user.dinner[5] = int(request.POST.get("thu_d", "0")) if request.POST.get("thu_d", "0") != "" else 0

    user.save()

    return HttpResponse("changed")


@login_required(login_url='/')
def change_food_order(request):
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


@login_required(login_url='/')
def change_email(request):
    # TODO : check email format
    request.user.email = request.POST.get("new_email")
    request.user.save()
    return HttpResponse("changed")


