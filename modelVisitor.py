# -*- coding: utf-8 -*-
from google.appengine.ext import db
__author__ = 'Daria'


class Organizer(db.Model):
    user = db.UserProperty(auto_current_user_add=False)
    nickname = db.StringProperty(required=False, multiline=False)
    contact = db.StringProperty(required=False)


class Command(db.Model):
    name = db.StringProperty()
    territory = db.StringProperty(multiline=False)

class Leader(db.Model):
    user = db.UserProperty(auto_current_user_add=True)
    command = db.ReferenceProperty(Command)
    nickname = db.StringProperty(multiline=False)
    contact = db.EmailProperty(required=True)


class Member(db.Model):
    pass_to_edit = db.StringProperty(multiline=False)
    sex = db.StringProperty(multiline=False)
    nickname = db.StringProperty(multiline=False)
    surname = db.StringProperty(required=False, multiline=False)
    command = db.ReferenceProperty(Command, required=False)
    birthdate = db.IntegerProperty(required=True)
    qualification = db.StringProperty(choices=[u'Б/Р', u'IIIю', u'IIю', u'Iю', 'III', 'II', 'I',
                                                              u'КМС', u'МС', u'МСМК', u'ЗМС'], default=u'Б/Р')
