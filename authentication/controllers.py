from userpanel.models import UserCollection

__author__ = 'bardia'
from django.shortcuts import HttpResponse, redirect

from django.contrib import auth
from django.contrib.auth.models import User
from authentication import views
from bot.stubot import check


def signIn(request):
    if request.POST:
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')

        check_res = check((username,password))
        if not check_res[0]:
            return HttpResponse("wrong username or password")

        name = check_res[1]
        uni_id = check_res[2]

        user = User.objects.create_user(username, password=password)
        user.is_active = True
        user.save()

        newUserInMongo = UserCollection()
        newUserInMongo.userId = user.id
        newUserInMongo.name = name
        newUserInMongo.uni_id = uni_id
        newUserInMongo.stu_username = username
        newUserInMongo.stu_password = password
        newUserInMongo.save()

        return HttpResponse("post")
    else:
        return views.signIn(request)



def login(request):
    if request.POST:
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        next = request.POST.get("next", '')

        user = None
        if password != '' and username != '':
            user = auth.authenticate(username=username, password=password)

        if user is not None:
            # the password verified for the user
            print("User is valid, active and authenticated")
            auth.login(request, user)
            return redirect(next)
        else:
            # the authentication system was unable to verify the username and password
            return HttpResponse("The username and password were incorrect.")
    else:
        return views.login(request)


def logout(request):
    auth.logout(request)
    return redirect('/')