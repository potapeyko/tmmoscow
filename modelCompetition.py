# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from google.appengine.ext import db
from modelVisitor import Member, Organizer
__author__ = 'Daria'


class Org:
    fio = 'fio'
    dol = 'dol'
    contact = 'cont'

    def __init__(self, f, d, c):
        self.fio = f
        self.dol = d
        self.contact = c


class MemInfo(db.Model):
    salary = db.FloatProperty(default=0)
    age_min = db.IntegerProperty(default=6)
    age_max = db.IntegerProperty(default=90)
    qual_min = db.StringProperty(multiline=False, default=u'б/р')
    qual_max = db.StringProperty(multiline=False, default=u'ЗМС')


class Competition(db.Model):
    name = db.StringProperty(multiline=False, default=u'Название соревнований')
    d_start = db.DateProperty(required=True)
    d_finish = db.DateProperty(required=True)
    days_count = db.IntegerProperty(default=1)
    #places = db.ListProperty(str)
    statistic = db.ListProperty(bool, default=[True, True, True])


class Distance(db.Model):
    competition = db.ReferenceProperty(Competition)
    day_numb = db.IntegerProperty(default=1)
    type = db.StringProperty()
    lent = db.StringProperty()


class DistInfo(db.Model):
    group_name = db.StringProperty(default=u'МЖЭ')
    length = db.FloatProperty(default=0)
    dist_class = db.IntegerProperty(default=1)
    min_com = db.IntegerProperty(default=1)
    max_com = db.IntegerProperty(default=1)
    mem_info = db.ReferenceProperty(MemInfo)
    distance = db.ReferenceProperty(Distance)


class CompMemb(db.Model):
    competition = db.ReferenceProperty(Competition)
    member = db.ReferenceProperty(Member)


class Info(db.Model):
    competition = db.ReferenceProperty(Competition)
    day_numb = db.IntegerProperty(default=1)
    place_addr = db.StringProperty()
    #place_img = db.BlobProperty()
    pz_is_open = db.BooleanProperty(default=True)
    pz_add_end = db.DateProperty(default=datetime.today()+timedelta(weeks=4))
    pz_change_end = db.DateProperty(default=datetime.today()+timedelta(weeks=4))
    tz_is_on = db.BooleanProperty(default=False)
    link = db.StringProperty()
    orgs = db.ListProperty(str)


