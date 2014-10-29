from mongoengine import *
import datetime

connect('Garson')


class UserCollection(Document):
    name = StringField(max_length=75, required=True)
    stu_username = StringField(max_length=8, required=True)
    stu_password = StringField(max_length=20, required=True)
    food_list_1 = ListField()
    food_list_2 = ListField()
    food_list_3 = ListField()
    user_id = IntField(required=True)
    credit = IntField(default=0)

    breakfast = ListField()
    lunch = ListField()
    dinner = ListField()

    reserved_food = ListField(ListField())

    today_meal_last_update = DateTimeField()

    @classmethod
    def _update_today_meal(cls):
        pass



if __name__ == "__main__":
    from bot.scraper import today_food
    user = UserCollection.objects(stu_username="92521114", stu_password="0017578167")[0]
    today = datetime.datetime.now().date()
    if not today == user.today_meal_last_update.date():
        user.today_lunch = today_food(("92521114", "0017578167"))
        user.today_meal_last_update = today
        user.save()

    print(user.today_lunch)
