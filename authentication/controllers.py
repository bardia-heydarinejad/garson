import datetime
from userpanel.models import UserCollection

__author__ = 'bardia'
from django.shortcuts import redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from bot.scraper import check, credit
from configuration.models import Food

def login(request):
    if request.POST:
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        next_url = request.POST.get("next", '')
        next_url = '/account' if next_url == "" else next_url

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
            check_res = check(username, password)
            if not check_res[0]:
                return HttpResponse(check_res[1]+check_res[2])
                return redirect("/?msg=wrong_user_pass")

            name = check_res[1]
            uni_id = check_res[2]

            if uni_id != username:
                return redirect("/?msg=wrong_uni_id")  # todo: set messesge

            user = User.objects.create_user(username=username, password=password)
            user.is_active = True

            if len(UserCollection.objects(stu_username=username)) == 1:
                user.save()
                return redirect(next_url)

            new_user_in_mongo = UserCollection()
            new_user_in_mongo.user_id = user.id
            new_user_in_mongo.name = name
            new_user_in_mongo.stu_username = username
            new_user_in_mongo.stu_password = password
            new_user_in_mongo.credit = credit(username, password)
            new_user_in_mongo.breakfast = [0, 0, 0, 0, 0, 0]
            new_user_in_mongo.lunch = [0, 0, 0, 0, 0, 0]
            new_user_in_mongo.dinner = [0, 0, 0, 0, 0, 0]
            new_user_in_mongo.food_list_2 = Food.get_all_id()
            new_user_in_mongo.food_list_1 = []
            new_user_in_mongo.food_list_3 = []
            new_user_in_mongo.today_meal_last_update = datetime.datetime.now().date()

            new_user_in_mongo.save()
            user.save()

            print("Registered successfully")
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(next_url)
    else:
        return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')


def flush():
    for user in User.objects.all():
        print("WARN -\t Deleting user - {}".format(user.username))
        user.delete()
    UserCollection.drop_collection()


def sync_mongo_sqlite():
    for user in User.objects.all():
        if len(user.username) == 8 and len(UserCollection.objects(stu_username=user.username)) == 0:
            user.delete()
            print('delete', user.username)

    for user_in_mongo in UserCollection.objects():
        username = user_in_mongo.stu_username
        password = user_in_mongo.stu_password
        user = User.objects.create_user(username=username, password=password)
        user.is_active = True
        user.save()


def duchp():
    for user in UserCollection.objects():
        if not check(user.stu_username, user.stu_password)[0]:
            print("WARN -\t Deleting user {}\n".format(user.stu_username))
            User.objects.get(username=user.stu_username).delete()
            user.delete()
        else:
            print("INFO -\t User {} checked\n".format(user.stu_username))


def delete(username):
    User.objects.get(username=username).delete()
    UserCollection.objects(stu_username=username)[0].delete()
