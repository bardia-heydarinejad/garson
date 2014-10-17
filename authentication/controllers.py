from userpanel.models import UserCollection

__author__ = 'bardia'
from django.shortcuts import HttpResponse, redirect

from django.contrib import auth
from django.contrib.auth.models import User
from authentication import views
from bot.scraper import check, credit
from configuration.models import Food


def login(request):
    if request.POST:
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        next_url = request.POST.get("next", '')

        user = None
        if password != '' and username != '':
            user = auth.authenticate(username=username, password=password)

        if user is not None:
            # the password verified for the user
            print("User is valid, active and authenticated")
            auth.login(request, user)
            return redirect(next_url)
        else:
            print("Not registerd try to register")
            check_res = check((username, password))
            if not check_res[0]:
                print("wrong user or pass to register")
                return HttpResponse("wrong username or password")

            name = check_res[1]
            uni_id = check_res[2]

            user = User.objects.create_user(username, password=password)
            user.is_active = True

            new_user_in_mongo = UserCollection()
            new_user_in_mongo.user_id = user.id
            new_user_in_mongo.name = name
            new_user_in_mongo.uni_id = uni_id
            new_user_in_mongo.stu_username = username
            new_user_in_mongo.stu_password = password
            new_user_in_mongo.credit = credit((username, password))
            new_user_in_mongo.food_list_2 = [x.id for x in Food.all_foods()]

            new_user_in_mongo.save()
            user.save()
            print "Registered successfully"
            return redirect(next_url)
    else:
        return views.login(request)


def logout(request):
    auth.logout(request)
    return redirect('/')


def flush():
    for user in User.objects.all():
        user.delete()
    UserCollection.drop_collection()
