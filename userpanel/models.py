from mongoengine import *

connect('Garson')


class UserCollection(Document):
    uni_id = StringField(max_length=8)
    name = StringField(max_length=75)
    stu_username = StringField(max_length=20)
    stu_password = StringField(max_length=20)
    food_list_1 = ListField()
    food_list_2 = ListField()
    food_list_3 = ListField()
    user_id = IntField(required=True)
    credit = IntField(default=0)
    sat = IntField(default=0)
    sun = IntField(default=0)
    mon = IntField(default=0)
    tue = IntField(default=0)
    wed = IntField(default=0)
    thu = IntField(default=0)
    fri = IntField(default=0)