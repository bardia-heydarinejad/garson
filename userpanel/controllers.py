from django.views.decorators.http import require_http_methods
from django.shortcuts import HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from userpanel.models import UserCollection
from django.views.decorators.csrf import csrf_exempt
from configuration.models import Food

__author__ = 'bardia'


@login_required(login_url='/')
@csrf_exempt
@require_http_methods(["POST"])
def change_days(request):
    us = UserCollection.objects(stu_username=request.user.username)
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

    print(user.lunch)
    user.save()

    return HttpResponse("changed")


@login_required(login_url='/')
@csrf_exempt
@require_http_methods(["POST"])
def change_food_order(request):
    us = UserCollection.objects(stu_username=request.user.username)
    if len(us) != 1:
        return HttpResponse("not active")
    user = us[0]
    l1 = [int(food_id) for food_id in request.POST.get("food_list_1", "").split()]
    l2 = [int(food_id) for food_id in request.POST.get("food_list_2", "").split()]
    l3 = [int(food_id) for food_id in request.POST.get("food_list_3", "").split()]

    if len((set(l1) | set(l2) | set(l3)) - set(Food.get_all_id())) > 0:
        HttpResponse("invalid id")

    # Add other foods
    if (set(l1) | set(l2)) | set(l3) != set(Food.get_all_id()):
        l2 = l2 + list(set(Food.get_all_id()) - (set(l1) | set(l2)) | set(l3))

    # Remove intersects
    if len(set(l2) & set(l1)) > 0:
        l1 = list(set(l1) - set(l2))

    if len(set(l2) & set(l3)) > 0:
        l3 = list(set(l1) - set(l2))

    if len(set(l3) & set(l1)) > 0:
        l1 = list(set(l1) - set(l3))

    # Remove repeated element
    if len(l1) != len(set(l1)):
        l1 = list(set(l1))

    if len(l2) != len(set(l2)):
        l2 = list(set(l2))

    if len(l3) != len(set(l3)):
        l3 = list(set(l3))

    user.food_list_1 = l1
    user.food_list_2 = l2
    user.food_list_3 = l3
    user.save()
    return HttpResponse("ثبت شد")


@login_required(login_url='/')
def change_email(request):
    email = request.POST.get("new_email")
    import re

    if re.match(r"\w+[a-zA-z0-9\.]+@[a-zA-z0-9\.]+\.\w+", email):
        request.user.email = email
        request.user.save()
    from bot.mandrill_mail import MandrillContact, MandrillEmail

    MandrillEmail().send(u"ثبت ایمیل", u"ایمیل شما با موفقیت ثبت شد. با تشکر. گروه ریشه", [MandrillContact("", email)])
    return redirect("/account")




