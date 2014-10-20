from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
from userpanel.models import UserCollection
from configuration.models import Food, Self
from json import dumps

def format_price(price):
    price = str(price / 10)
    l = len(price)
    new_format = ""
    for i in range(1, l + 1):
        new_format = price[l - i] + new_format
        if i % 3 == 0:
            new_format = ',' + new_format
    return new_format


@login_required(login_url='/')
def user_panel(request):
    us = UserCollection.objects(user_id=request.user.id)
    if len(us) != 1:
        return HttpResponse("Wrong")

    name = us[0].name if us[0].name is not None else ""
    stu_credit = us[0].credit if us[0].credit is not None else 0
    uni_id = us[0].uni_id if us[0].uni_id is not None else '00000000'

    food_list_name_1 = []
    food_list_name_2 = []
    food_list_name_3 = []

    for food_id in us[0].food_list_1:
        food_list_name_1.append(Food.get_name(food_id))
    for food_id in us[0].food_list_2:
        food_list_name_2.append(Food.get_name(food_id))
    for food_id in us[0].food_list_3:
        food_list_name_3.append(Food.get_name(food_id))

    print us[0].breakfast

    email = request.user.email if request.user.email is not None else ''
    # week = [us[0].sat,us[0].sun,]
    #
    # c = credit
    # days = 0
    #
    # while c>0:

    aaa = Self.get_all()
    for i in aaa:
        print i.id_,i.name

    print aaa

    data = {"name": name, 'uni_id': uni_id, 'credit': format_price(stu_credit),
            'email': email, 'food_list_name_1': food_list_name_1,
            'food_list_name_2': food_list_name_2, 'food_list_name_3': food_list_name_3,
            'all_selves': aaa, 'breakfast': us[0].breakfast,
            'lunch': us[0].lunch, 'dinner': us[0].dinner}
    return render(request, "user.html", data)


@login_required(login_url='/')
def credit(request):
    us = UserCollection.objects(user_id=request.user.id)
    if len(us) == 1:
        return HttpResponse([0].credit if us[0].credit is not None else 0)