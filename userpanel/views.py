from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from userpanel.models import UserCollection
from configuration.models import Food, Self
from authentication.controllers import sync_mongo_sqlite


def format_price(price):
    price = str(int(price / 10))
    l = len(price)
    new_format = ""
    for i in range(1, l + 1):
        new_format = price[l - i] + new_format
        if i % 3 == 0:
            new_format = ',' + new_format
    return new_format


@login_required(login_url='/')
def user_panel(request):
    us = UserCollection.objects(stu_username=request.user.username)
    if len(us) != 1:
        sync_mongo_sqlite()
        return redirect('/?msg=invalid_id')
    user = us[0]

    name = user.name if user.name is not None else ""
    stu_credit = user.credit if user.credit is not None else 0
    uni_id = user.stu_username if user.stu_username is not None else '00000000'

    food_list_1 = []
    food_list_2 = []
    food_list_3 = []

    for food_id in user.food_list_1:
        food_list_1.append(Food(food_id, Food.get_name(food_id)))
    for food_id in user.food_list_2:
        food_list_2.append(Food(food_id, Food.get_name(food_id)))
    for food_id in user.food_list_3:
        food_list_3.append(Food(food_id, Food.get_name(food_id)))

    l1 = [int(food_id) for food_id in user.food_list_1]
    l2 = [int(food_id) for food_id in user.food_list_2]
    l3 = [int(food_id) for food_id in user.food_list_3]
    if (set(l1) | set(l2)) | set(l3) != set(Food.get_all_id()):
        l3 = list(set(l3) | set(Food.get_all_id()) - (set(l1) | set(l2)) | set(l3))
        user.food_list_3 = l3
        user.save()

    email = request.user.email if request.user.email is not None else ''

    aaa = Self.get_all()
    data = {"name": name, 'uni_id': uni_id, 'credit': format_price(stu_credit),
            'email': email, 'food_list_name_1': food_list_1,
            'food_list_name_2': food_list_2, 'food_list_name_3': food_list_3,
            'all_selves': aaa, 'breakfast': user.breakfast,
            'lunch': user.lunch, 'dinner': user.dinner}
    return render(request, "user.html", data)
