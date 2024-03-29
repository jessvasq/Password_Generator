from flask_login import UserMixin
from peewee import *


database = SqliteDatabase('User.sqlite')
'''User Model'''
#This model represents your user objects and shuld include methods to load users from the user ID and verify their password
class User(UserMixin, Model):
    id = AutoField(primary_key=True)
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    
    class Meta:
        database = database
        
        
class Item(Model):
    id = AutoField(primary_key=True)
    title = CharField()
    username = CharField()
    password = CharField()
    website = CharField()
    email = CharField()
    category = CharField()
    user = ForeignKeyField(User, backref='items')
    
    class Meta:
        database = database

def initialize():
    database.connect()
    database.create_tables([User, Item], safe=True)
    print('tables created')
    database.close()