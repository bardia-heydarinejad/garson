from userpanel.models import UserCollection

__author__ = 'bardia'
from django.shortcuts import HttpResponse, redirect

from django.contrib import auth
from django.contrib.auth.models import User
from authentication import views


def signIn(request):
    if request.POST:
        email = request.POST.get("email", '')
        password = request.POST.get("password", '')
        re_password = request.POST.get("re_password", '')
        if password != re_password:
            return HttpResponse("password does not match")

        # Generate hash
        import hashlib

        hash_object = hashlib.md5('<' + email + '>')

        user = User.objects.create_user(email=email, password=password)
        user.is_active = False
        user.hash = hash_object.hexdigest()
        user.save()
        return HttpResponse("post")
    else:
        return views.signIn(request)


def activeUser(request):
    email = request.GET.get("email")
    code = request.GET.get("code")
    if email is None or code is None:
        return HttpResponse("Failed")
    user = User.objects.get(email=email)
    import hashlib

    hash_object = hashlib.md5('<' + user.email + '>')

    if code == hash_object.hexdigest() and not user.is_active:
        user.is_active = True
        newUserInMongo = UserCollection()
        newUserInMongo.userId = user.id
        newUserInMongo.save()
        return HttpResponse("activated")
    return HttpResponse("404")

def debugActiveUser(request):
    user = request.user
    if not user.is_active:
        user.is_active = True
        newUserInMongo = UserCollection()
        newUserInMongo.userId = user.id
        newUserInMongo.save()
        return HttpResponse("activated")
    return HttpResponse("was active")


def login(request):
    if request.POST:
        username_or_email = request.POST.get("username_or_email", '')
        password = request.POST.get("password", '')
        next = request.POST.get("next", '')

        user = None
        if password != '' and username_or_email != '':
            user = auth.authenticate(username=username_or_email, password=password)
            if user is None:
                user = auth.authenticate(email=username_or_email, password=password)

        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
                auth.login(request, user)
                return redirect(next)
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
    else:
        return views.login(request)


def logout(request):
    auth.logout(request)
    return redirect('/')