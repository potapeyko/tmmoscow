# -*- coding: utf-8 -*-
__author__ = 'Daria'

from google.appengine.api import users
from datetime import date, datetime
from google.appengine.api import images
from modelCompetition import MemInfo, DistInfo, Competition, Distance, Info, Org
from modelVisitor import Organizer, Leader, Member
from google.appengine.ext import db
import os
import jinja2
import webapp2
from CompetitionHandlers import formatDateList


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Team(webapp2.RequestHandler):
    def get(self):      # displays info about team for that leader and all members
        self.response.write('GET from Team')

        #Add this to LOGIN link: users.create_login_url(dest_url='/postSignIn')

    def post(self):     # changes team info
        self.response.write('POST from Team')


class AddMemberToTeam(webapp2.RequestHandler):
    def get(self):      # displays empty form for adding new member to command
        self.response.write('GET from AddMemberToTeam')

    def post(self):     # saves new member to db
        self.response.write('POST from AddMemberToTeam')
