from mongoengine import *
import datetime

connect('Garson')


class CookieCollection(Document):
    cookie = StringField(max_length=200, required=True)
    time = DateTimeField()
