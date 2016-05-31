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
import OtherHandlers


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Team(webapp2.RequestHandler):
    def get(self):      # displays info about team for that leader and all members
        user = users.get_current_user()
        if not user:
            self.response.write('Error 401: you are unauthorized! (Team:get)')
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.findUser(email)
            roles = OtherHandlers.createRolesHead(is_org, is_lead, is_memb)
            if is_lead and OtherHandlers.cur_role == 'leader':
                self.response.write('Team Info for Leader')
            else:
                self.response.write('You can\'t look Team Info because you are not a leader')

    def post(self):     # changes team info
        user = users.get_current_user()
        if not user:
            self.response.write('Error 401: you are unauthorized! (Team:post)')
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.findUser(email)
            roles = OtherHandlers.createRolesHead(is_org, is_lead, is_memb)
            if is_lead and OtherHandlers.cur_role == 'leader':
                self.response.write('Save changes of Team Info for Leader')
            else:
                self.response.write('You can\'t change Team Info because you are not a leader')


class AddMemberToTeam(webapp2.RequestHandler):
    def get(self):      # displays empty form for adding new member to command
        user = users.get_current_user()
        if not user:
            self.response.write('Error 401: you are unauthorized! (AddMemberTeam:get)')
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.findUser(email)
            roles = OtherHandlers.createRolesHead(is_org, is_lead, is_memb)
            if is_lead and OtherHandlers.cur_role == 'leader':
                self.response.write('Fill in form to add new member to your team, Leader')
            else:
                self.response.write('You can\'t add new Member to Team because you are not a leader')


    def post(self):     # saves new member to db
        user = users.get_current_user()
        if not user:
            self.response.write('Error 401: you are unauthorized! (AddMemberTeam:post)')
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.findUser(email)
            roles = OtherHandlers.createRolesHead(is_org, is_lead, is_memb)
            if is_lead and OtherHandlers.cur_role == 'leader':
                self.response.write('Saving new member to your team, Leader')
            else:
                self.response.write('You can\'t save new Member to Team because you are not a leader')
