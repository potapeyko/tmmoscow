# -*- coding: utf-8 -*-
__author__ = 'Daria'

from google.appengine.ext import db

class Organizer(db.Model):
    user = db.UserProperty(required=True, auto_current_user_add = True)

    nickname = db.StringProperty(required=False, multiline=False)
    contact = db.StringProperty(required=False)

class Leader(db.Model):
    user = db.UserProperty(required=True, auto_current_user_add=True)
    command = db.StringProperty(required=True, multiline=False, default=u'Отсутствует')
    territory = db.StringProperty(required=True, multiline=False, default=u'Отсутствует')

    nickname = db.StringProperty(required=True, multiline=False)
    contact = db.EmailProperty(required=True)

class Member(db.Model):
    passToEdit = db.StringProperty(multiline=False)
    leader = db.ReferenceProperty(Leader)
    nickname = db.StringProperty(required=True, multiline=False)
    surname = db.StringProperty(required=False, multiline=False)
    command = db.StringProperty(required=True, multiline=False, default=u'Отсутствует')
    territory = db.StringProperty(required=True, multiline=False, default=u'Отсутствует')
    birthdate = db.IntegerProperty(required=True)
    qualification = db.StringProperty(required=True, choices=[u'Б/Р', u'IIIю', u'IIю', u'Iю', 'III', 'II', 'I',
                                                             u'КМС', u'МС', u'МСМК', u'ЗМС'], default=u'Б/Р')

