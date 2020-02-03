from mongoengine import *
connect(db='quick-entry', host='mongodb+srv://lernen:sro0dcS2bvcFDUIf@cluster0-durfo.mongodb.net/lernen?retryWrites=true&w=majority')


class Course(Document):
    name = StringField(required=True, unique=True)
    enrolled_num = IntField(default=0)
    videos = ListField(ReferenceField('Video'))
    admin = ReferenceField('Admin')
    imageURL = StringField(required=True)
    description = StringField(required=True)

class Video(Document):
    name = StringField(required=True)
    views = IntField(default=0)
    course = ReferenceField('Course')
    url = StringField(required=True)


class Room(Document):
    name = StringField(required=True)
    roomnumber = IntField(required=True)
    capacity = IntField(required=True)
    current = IntField(default=0)
    entrylist = ListField(ReferenceField('Entry')) #String used, since Entry class is defined after Room


class User(Document):

    username = StringField(required=True, unique=True)
    fullname = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    current_course = ReferenceField(Course)
    enrolled = ListField(ReferenceField(Course))


class Entry(Document):

    user = ReferenceField(User)
    room = ReferenceField(Room)
    timestamp = LongField()
    exittime = LongField()

class Admin(Document):

    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    fname = StringField(required=True)
    email = StringField(required=True, unique=True)
    courses = ListField(ReferenceField('Course'))