# -*- coding: utf-8 -*-

from google.appengine.api import users
import os
import jinja2
import webapp2
import time
from google.appengine.ext import db
from modelVisitor import Member
from modelCompetition import Competition
from LeaderHandlers import saltPass

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MemberInfo(webapp2.RequestHandler):
    def get(self):      # displays info about certain member or empty form for adding new member
        login = users.create_login_url(dest_url='/postSignIn')
        comp_key = self.request.GET['competition']
        memb_key = self.request.GET['member']
        member = Member.get(memb_key)
        name = member.surname.split(' ')[1]
        surname = member.surname.split(' ')[0]
        temp_values = {'login': login, 'logout': users.create_logout_url('/login'), 'surname': surname, 'name': name,
                       'age': member.birthdate, 'qual': member.qualification, 'team': member.command, 'competition':
                       comp_key, 'memb_key': memb_key}
        template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/member/MemberView.html')
        self.response.write(template.render(temp_values))

    def post(self):     # saves new member or changes
        comp_key = self.request.POST.get('competition')
        passwd = self.request.POST.get('changePass')
        memb_key = self.request.POST.get('member')
        member = Member.get(memb_key)
        if saltPass(passwd) == member.pass_to_edit:
            surname = self.request.POST.get('surnameMemb') + ' ' + self.request.POST.get('nameMemb')
            age = int(self.request.POST.get('ageMemb'))
            qual = self.request.POST.get('qualMemb')
            member.surname = surname
            member.birthdate = age
            member.qualification = qual
            member.save()
            time.sleep(0.1)
            self.redirect('/entryOneMemb?competition='+comp_key)
        else:
            login = users.create_login_url(dest_url='/postSignIn')
            name = member.surname.split(' ')[1]
            surname = member.surname.split(' ')[0]
            temp_values = {'login': login, 'logout': users.create_logout_url('/login'), 'surname': surname,
                           'name': name, 'age': member.birthdate, 'qual': member.qualification, 'team': member.command,
                           'competition': comp_key, 'memb_key': memb_key, 'tooltip': u'Неверный пароль подтверждения. Попробуйте еще раз'}
            template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/member/MemberView.html')
            self.response.write(template.render(temp_values))


class MemberToComp(webapp2.RequestHandler):
    def get(self):     # displays list of all members in system to check to competition
        login = users.create_login_url(dest_url='/postSignIn')
        comp_key = self.request.GET['competition']
        comp = Competition.get(comp_key)
        membs = db.Query(Member).order('surname')
        keys = []
        for m in membs:
            keys.append(m.key())
        temp_values = {'login': login, 'logout': users.create_logout_url('/login'), 'name': comp.name, 'membs_count':
                       membs.count(), 'membs': membs, 'keys': keys, 'competition': comp_key}
        template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/member/MemberList.html')
        self.response.write(template.render(temp_values))


class ChangeMember(webapp2.RequestHandler):
    def post(self):
        self.response.write('POST from ChangeMember (member)')


class AddMembToGroup(webapp2.RequestHandler):
    def post(self):
        self.response.write('POST from AddMembToGroup (member)')


class EnterMember(webapp2.RequestHandler):
    def post(self):
        self.response.write('POST from EnterMember (member)')
