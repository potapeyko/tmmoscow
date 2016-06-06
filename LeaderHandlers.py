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
import random
import string
import hashlib
import time


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
                team.name = newName
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
            temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                           'login_redir': users.create_login_url('/postSignIn')}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.findUser(email)
            roles = OtherHandlers.createRolesHead(is_org, is_lead, is_memb)
            if is_lead and OtherHandlers.cur_role == 'leader':
                pass_to_edit = generatePass()
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'edit_pass': pass_to_edit, 'card_title': u'Новый участник команды', 'new_memb': True}
                template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/leader/Member.html')
            else:
                temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                               'login_redir': users.create_login_url('/postSignIn')}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
        self.response.write(template.render(temp_values))


    def post(self):     # saves new member to db
        user = users.get_current_user()
        if not user:
            temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                           'login_redir': users.create_login_url('/postSignIn')}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
            self.response.write(template.render(temp_values))
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.findUser(email)
            if is_lead and OtherHandlers.cur_role == 'leader':
                surname = self.request.POST.get('surnameMemb')
                birthdate = int(self.request.POST.get('birthdate'))
                qual = self.request.POST.get('qualMemb')
                sex = self.request.POST.get('sexMemb')
                pass_to_edit = saltPass(self.request.POST.get('passToEdit'))
                team = db.Query(Leader).filter('user =', user).get().command
                member = Member(pass_to_edit=pass_to_edit, sex=sex, surname=surname, birthdate=birthdate,
                                qualification=qual, command=team)
                member.put()
                time.sleep(0.1)
                self.redirect('/reg/leaderTeam')
            else:
                temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                               'login_redir': users.create_login_url('/postSignIn')}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
                self.response.write(template.render(temp_values))


class ChangeMember(webapp2.RequestHandler):
    def get(self):      # displays form with old member's data
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
                memb_key = self.request.get('change')
                member = db.get(memb_key)
                sex_m = ''
                sex_w = ''
                if member.sex == u'Мужской':
                    sex_m = 'checked'
                else:
                    sex_w = 'checked'
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'card_title': u'Изменение участника', 'memb_name':
                               member.surname, 'birthdate': member.birthdate, 'qual': member.qualification, 'sex_m':
                               sex_m, 'sex_w': sex_w, 'new_memb': False, 'memb_key': memb_key, 'change': memb_key}
                template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/leader/Member.html')
            else:
                temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                               'login_redir': users.create_login_url('/postSignIn')}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
        self.response.write(template.render(temp_values))

    def post(self):     # saves member's changes to db and redirects to team page
        user = users.get_current_user()
        if not user:
            temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                           'login_redir': users.create_login_url('/postSignIn')}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
            self.response.write(template.render(temp_values))
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.findUser(email)
            if is_lead and OtherHandlers.cur_role == 'leader':
                memb_key = self.request.POST.get('change')
                member = db.get(memb_key)
                member.surname = self.request.POST.get('surnameMemb')
                member.birthdate = int(self.request.POST.get('birthdate'))
                member.qualification = self.request.POST.get('qualMemb')
                member.sex = self.request.POST.get('sexMemb')
                member.put()
                time.sleep(0.1)
                self.redirect('/reg/leaderTeam')
            else:
                temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                               'login_redir': users.create_login_url('/postSignIn')}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
                self.response.write(template.render(temp_values))


class DeleteMember(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not user:
            temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                           'login_redir': users.create_login_url('/postSignIn')}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
            self.response.write(template.render(temp_values))
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.findUser(email)
            if is_lead and OtherHandlers.cur_role == 'leader':
                memb_key = self.request.POST.get('delete')
                member = db.delete(memb_key)
                time.sleep(0.1)
                self.redirect('/reg/leaderTeam')
            else:
                temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                               'login_redir': users.create_login_url('/postSignIn')}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
                self.response.write(template.render(temp_values))


# Generates random 8-symbol password
def generatePass():
    rid = ''
    for x in range(8):
        rid += random.choice(string.ascii_letters + string.digits)
    return rid

def saltPass(paswd):
    md = hashlib.md5()
    md.update(paswd)
    md.update('dado')       # This is salt
    return md.hexdigest()


