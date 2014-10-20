from mongoengine import *

connect('Garson')


class UserCollection(Document):
    uni_id = StringField(max_length=8, required=True)
    name = StringField(max_length=75, required=True)
    stu_username = StringField(max_length=20, required=True)
    stu_password = StringField(max_length=20, required=True)
    food_list_1 = ListField()
    food_list_2 = ListField()
    food_list_3 = ListField()
    user_id = IntField(required=True)
    credit = IntField(default=0)

    breakfast = ListField()
    lunch = ListField()
    dinner = ListField()