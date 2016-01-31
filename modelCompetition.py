# -*- coding: utf-8 -*-
__author__ = 'Daria'

from datetime import datetime
from google.appengine.ext import db
from models.Visitor import Member, Organizer

class MemInfo(db.Model):
    salary = db.FloatProperty(required=True, default=0)
    age_min = db.IntegerProperty(required=True, default=6)
    age_max = db.IntegerProperty(required=True, default=90)
    qual_min = db.StringProperty(required=True, choices=[u'Б/Р', u'IIIю', u'IIю', u'Iю', 'III', 'II', 'I',
                                                             u'КМС', u'МС', u'МСМК', u'ЗМС'], default=u'Б/Р')
    qual_max = db.StringProperty(required=True, choices=[u'Б/Р', u'IIIю', u'IIю', u'Iю', 'III', 'II', 'I',
                                                             u'КМС', u'МС', u'МСМК', u'ЗМС'], default=u'ЗМС')

class DistInfo(db.Model):
    group_name = db.StringProperty(required=True, default=u'МЖЭ')
    length = db.FloatProperty(required=True, default=0)
    distClass = db.StringProperty(required=True, choices=['1', '2', '3', '4', '5', '6'], default='1')
    min_com = db.IntegerProperty(required=True, default=1)
    max_com = db.IntegerProperty(required=True, default=1)
    memInfo = db.ReferenceProperty(MemInfo)

class Distance(db.Model):
    comp_id = db.ReferenceProperty(Competition)
    day_numb = db.IntegerProperty(required=True, default=1)
    type = db.StringProperty(required=True, choices=['g', 's', 'l'], default='l')
    length = db.StringProperty(required=True, choices=['l', 's'], default='s')
    distInfo = db.ListProperty(DistInfo, required=True, default=DistInfo())

class Info(db.Model):
    comp_id = db.ReferenceProperty(Competition)
    day_numb = db.IntegerProperty(required=True, default=1)
    place_addr = db.StringProperty(required=False)
    place_img = db.BlobProperty(required=False)
    pzIsOpen = db.BooleanProperty(required=True, default=True)
    pzAddEnd = db.DateProperty(required=True, default=datetime.today()+datetime.timdelta(month=1))
    pzChangeEnd = db.DateProperty(required=True, default=datetime.today()+datetime.timdelta(month=1))
    tzIsOn = db.BooleanProperty(required=True, default=False)
    link = db.LinkProperty(required=True, default=u'http://tmmoscow.ru/')
    orgs = db.ListProperty(Organizer, required=True, default=[])
    dols = db.ListProperty(str, required=True, default=[])


class Competition(db.Model):
    name = db.StringProperty(required=True, multiline=False, default=u'Название соревнований')
    logo = db.BlobProperty(required=False)
    d_start = db.DateProperty(required=True)
    d_finish = db.DateProperty(required=True)
    days_count = db.IntegerProperty(required=True, default=1)
    places = db.ListProperty(str, required=False)
    statistic = db.ListProperty(bool, required=True, default=[True, True, True, True, True])
    members = db.ListProperty(Member, required=True, default=[])