__author__ = 'bardia'
from django.shortcuts import  HttpResponse ,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from authentication import views

def signIn(request):
    if request.POST:
        username = request.POST.get("username",'')
        email = request.POST.get("email",'')
        password = request.POST.get("password",'')
        re_password = request.POST.get("re_password",'')
        if(len(username) != 8):
            return HttpResponse("username not valid")
        if(password != re_password):
            return HttpResponse("password does not match")
        user = User.objects.create_user(username, email, password)
        user.complete_registeration = False
        user.save()
        return HttpResponse("post")
    else:
        return views.signIn(request)

def login(request):
    if request.POST:
        username_or_email = request.POST.get("username_or_email",'')
        password = request.POST.get("password",'')
        next = request.POST.get("next",'')

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