# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from google.appengine.ext import db
from modelVisitor import Member, Organizer
__author__ = 'Daria'


class MemInfo(db.Model):
    salary = db.FloatProperty(default=0)
    age_min = db.IntegerProperty(default=6)
    age_max = db.IntegerProperty(default=90)
    qual_min = db.StringProperty(multiline=False, default=u'б/р')
    qual_max = db.StringProperty(multiline=False, default=u'ЗМС')


class DistInfo(db.Model):
    group_name = db.StringProperty(default=u'МЖЭ')
    length = db.FloatProperty(default=0)
    dist_class = db.IntegerProperty(default=1)
    min_com = db.IntegerProperty(default=1)
    max_com = db.IntegerProperty(default=1)
    mem_info = db.ReferenceProperty(MemInfo)


class Competition(db.Model):
    name = db.StringProperty(multiline=False, default=u'Название соревнований')
    d_start = db.DateProperty(required=True)
    d_finish = db.DateProperty(required=True)
    days_count = db.IntegerProperty(default=1)
    places = db.ListProperty(str)
    statistic = db.ListProperty(bool, default=[True, True, True, True, True])
    members = db.ReferenceProperty(Member)


class Distance(db.Model):
    comp_id = db.ReferenceProperty(Competition)
    day_numb = db.IntegerProperty(default=1)
    type = db.StringProperty(choices=['g', 's', 'l'], default='l')
    lent = db.StringProperty(choices=['l', 's'], default='s')
    distInfo = db.ReferenceProperty(DistInfo)


class Info(db.Model):
    comp_id = db.ReferenceProperty(Competition)
    day_numb = db.IntegerProperty(default=1)
    place_addr = db.StringProperty()
    place_img = db.BlobProperty()
    pzIsOpen = db.BooleanProperty(default=True)
    pzAddEnd = db.DateProperty(default=datetime.today()+timedelta(weeks=4))
    pzChangeEnd = db.DateProperty(default=datetime.today()+timedelta(weeks=4))
    tzIsOn = db.BooleanProperty(default=False)
    link = db.LinkProperty(default=u'http://tmmoscow.ru/')
    orgs = db.ReferenceProperty(Organizer)
    dols = db.ListProperty(str, default=[])
