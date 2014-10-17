from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
from userpanel.models import UserCollection


def format_price(price):
    price = str(price / 10)
    l = len(price)
    new_format = ""
    for i in range(1, l + 1):
        new_format = price[l - i] + new_format
        if i % 3 == 0:
            new_format = ',' + new_format
    return new_format


@login_required(login_url='/authentication/login/')
def userPanel(request):
    name = ""
    credit = 0
    us = UserCollection.objects(user_id=request.user.id)
    if len(us) == 1:
        name = us[0].name if us[0].name is not None else ""
        credit = us[0].credit if us[0].credit is not None else 0
    #     week = [us[0].sat,us[0].sun,]
    #
    # c = credit
    # days = 0
    #
    # while c>0:

    return render(request, "UserPanel.html", {"name": name, 'credit': format_price(credit)})


@login_required(login_url='/authentication/login/')
def credit(request):
    us = UserCollection.objects(user_id=request.user.id)
    if len(us) == 1:
        return HttpResponse([0].credit if us[0].credit is not None else 0)