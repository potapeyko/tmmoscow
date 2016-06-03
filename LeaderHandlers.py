# -*- coding: utf-8 -*-
__author__ = 'Daria'

from google.appengine.api import users
from datetime import date, datetime
from google.appengine.api import images
from modelCompetition import MemInfo, DistInfo, Competition, Distance, Info, Org
from modelVisitor import Organizer, Leader, Member, Command
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
            temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                           'login_redir': users.create_login_url('/postSignIn')}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.findUser(email)
            roles = OtherHandlers.createRolesHead(is_org, is_lead, is_memb)
            if is_lead and OtherHandlers.cur_role == 'leader':
                leader = db.Query(Leader).filter('user =', user).get()
                team = leader.command
                territory = team.territory
                membs = db.Query(Member).filter('command =', team)
                membs_count = membs.count()
                memb_keys = []
                for memb in membs:
                    memb_keys.append(memb.key())
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'team_name': team.name, 'terry': territory, 'membs': membs, 'membs_count': membs_count,
                               'keys': memb_keys}
                template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/leader/Team.html')
            else:
                temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                               'login_redir': users.create_login_url('/postSignIn')}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
        self.response.write(template.render(temp_values))

    def post(self):     # changes team info
        user = users.get_current_user()
        if not user:
            temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                           'login_redir': users.create_login_url('/postSignIn')}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.findUser(email)
            roles = OtherHandlers.createRolesHead(is_org, is_lead, is_memb)
            if is_lead and OtherHandlers.cur_role == 'leader':
                newName = self.request.POST.get('nameTeam')
                newTerry = self.request.POST.get('terryTeam')
                lead = db.Query(Leader).filter('user =', user).get()
                team = lead.command
                team.command = newName
                team.territory = newTerry
                team.put()
                membs = db.Query(Member).filter('command =', team)
                membs_count = membs.count()
                memb_keys = []
                for memb in membs:
                    memb_keys.append(memb.key())
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'team_name': newName, 'terry': newTerry, 'membs': membs, 'membs_count': membs_count,
                               'keys': memb_keys}
                template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/leader/Team.html')
            else:
                temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                               'login_redir': users.create_login_url('/postSignIn')}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
        self.response.write(template.render(temp_values))


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
