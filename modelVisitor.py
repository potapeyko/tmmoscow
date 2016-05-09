# -*- coding: utf-8 -*-
from google.appengine.ext import db
__author__ = 'Daria'


class Organizer(db.Model):
    nickname = db.StringProperty(required=True, multiline=False)       # email, unique in whole datastore. Used to reference to Google account
    fullname = db.StringProperty(required=False)
    contact = db.StringProperty(required=False)


class Leader(db.Model):
    nickname = db.StringProperty(multiline=False)                      # email, unique in whole datastore. Used to reference to Google account
    fullname = db.StringProperty(required=False)
    command = db.StringProperty(multiline=False, default=u'Отсутствует')
    territory = db.StringProperty(multiline=False, default=u'Отсутствует')
    contact = db.StringProperty(required=True)

class Member(db.Model):
    passToEdit = db.StringProperty(multiline=False)
    nickname = db.StringProperty(multiline=False)
    surname = db.StringProperty(required=False, multiline=False)
    command = db.StringProperty(multiline=False, default=u'Отсутствует')
    territory = db.StringProperty(multiline=False, default=u'Отсутствует')
    birthdate = db.IntegerProperty(required=True)
    qualification = db.StringProperty(multiline=False, required=True, default=u"б/р")

class LeadMemb(db.Model):
    leader = db.ReferenceProperty(Leader)
    member = db.ReferenceProperty(Member)
