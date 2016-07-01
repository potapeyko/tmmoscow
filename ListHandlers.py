# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
import time
from google.appengine.ext import db
from google.appengine.api import users

import OtherHandlers
from modelVisitor import Member, Organizer, Leader, Command
from Common import show_unauth_page, BaseHandler

__author__ = 'Daria'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

tooltip_message = ''
tooltip_show = 'none'


class OrganizersHandler(BaseHandler):

    def get(self):
        """Displays whole list of organizers"""
        user = users.get_current_user()
        if user:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            roles = OtherHandlers.create_roles_head(self, is_org, is_lead, is_memb)
            if is_org and self.session.get('role') == 'organizer':
                orgs = db.Query(Organizer).order('nickname')
                keys = []
                for org in orgs:
                    keys.append(org.key())
                global tooltip_message
                global tooltip_show
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                           'disp_tool': tooltip_show, 'tool': tooltip_message, 'organizers': orgs, 'keys': keys}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/OrganizerList.html')
            else:
                temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                               'login_redir': users.create_login_url('/reg/newCompetition')}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
            self.response.write(template.render(temp_values))
        else:
            show_unauth_page(self)

    def post(self):
        """Finds organizers by keyword"""
        user = users.get_current_user()
        if user:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            roles = OtherHandlers.create_roles_head(self, is_org, is_lead, is_memb)
            if is_org and self.session.get('role') == 'organizer':
                search_fio = self.request.POST['findOrganizer']
                orgs = db.Query(Organizer).filter('nickname >=', search_fio).filter('nickname <=', search_fio+'1')\
                            .order('nickname')
                keys = []
                for org in orgs:
                    keys.append(org.key())
                global tooltip_message
                global tooltip_show
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'disp_tool': tooltip_show, 'tool': tooltip_message, 'organizers': orgs, 'keys': keys}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/OrganizerList.html')
                self.response.write(template.render(temp_values))
            else:
                show_unauth_page(self)
        else:
            show_unauth_page(self)


class AddOrganizer(BaseHandler):

    def post(self):
        """Adds new organizer to list or changes existing"""
        if self.request.POST['olKey']:
            new_fio = self.request.POST['olFio']
            new_contact = self.request.POST['olContact']
            org_key = self.request.POST['olKey']
            organizer = Organizer.get(org_key)
            organizer.nickname = new_fio
            organizer.contact = new_contact
            organizer.put()
            tooltip_message = u'Организатор %s изменен' % new_fio
        else:
            fio = self.request.POST['olFio']
            contact = self.request.POST['olContact']
            new_org = Organizer(nickname=fio, contact=contact)
            new_org.put()
            global tooltip_message
            global tooltip_show
            tooltip_message = u'Организатор %s добавлен базу' % fio
        tooltip_show = 'block'
        time.sleep(0.1)
        self.redirect('/reg/organizerList')


class DeleteOrganizer(BaseHandler):

    def post(self):
        """Deletes organizer from list"""
        org_id = self.request.POST['idToDeleteChange']
        fio = self.request.POST['organFio']
        db.delete(org_id)
        time.sleep(0.1)
        global tooltip_message
        global tooltip_show
        tooltip_message = u'Организатор %s удален из базы' % fio
        tooltip_show = 'block'
        self.redirect('/reg/organizerList')


class LeadersHandler(BaseHandler):

    def get(self):
        """Displays whole list of leaders"""
        user = users.get_current_user()
        if user:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            roles = OtherHandlers.create_roles_head(self, is_org, is_lead, is_memb)
            if is_org and self.session.get('role') == 'organizer':
                leads = db.Query(Leader).order('nickname')
                keys = []
                for lead in leads:
                    keys.append(lead.key())
                global tooltip_message
                global tooltip_show
                tooltip_message = ''
                tooltip_show = 'none'
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'disp_tool': tooltip_show, 'tool': tooltip_message, 'leads': leads, 'keys': keys}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/LeaderList.html')
                self.response.write(template.render(temp_values))
            else:
                show_unauth_page(self)
        else:
            show_unauth_page(self)

    def post(self):
        """Finds leaders by keyword"""
        user = users.get_current_user()
        if user:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            roles = OtherHandlers.create_roles_head(self, is_org, is_lead, is_memb)
            if is_org and self.session.get('role') == 'organizer':
                search_fio = self.request.POST['findLeader']
                leads = db.Query(Leader).filter('nickname >=', search_fio).filter('nickname <=', search_fio+'1')\
                            .order('nickname')
                keys = []
                for org in leads:
                    keys.append(org.key())
                global tooltip_message
                global tooltip_show
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'disp_tool': tooltip_show, 'tool': tooltip_message, 'leads': leads, 'keys': keys}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/LeaderList.html')
                self.response.write(template.render(temp_values))
            else:
                show_unauth_page(self)
        else:
            show_unauth_page(self)


class AddLeader(BaseHandler):

    def post(self):
        """Adds new leader to list or changes existing"""
        if self.request.POST['llKey']:
            new_fio = self.request.POST['llFio']
            new_command = self.request.POST['llComand']
            new_terry = self.request.POST['llTerritory']
            new_contact = self.request.POST['llContact']
            lead_key = self.request.POST['llKey']
            leader = Leader.get(lead_key)
            leader.nickname = new_fio
            leader.contact = new_contact
            team = leader.command
            team.name = new_command
            team.territory = new_terry
            team.put()
            leader.put()
            tooltip_message = u'Руководитель %s изменен' % new_fio
        else:
            fio = self.request.POST['llFio']
            command = self.request.POST['llComand']
            terry = self.request.POST['llTerritory']
            contact = self.request.POST['llContact']
            team = Command(name=command, territory=terry)
            team.put()
            new_lead = Leader(nickname=fio, command=team, contact=contact)
            new_lead.put()
            global tooltip_message
            global tooltip_show
            tooltip_message = u'Руководитель %s добавлен базу' % fio
        tooltip_show = 'block'
        time.sleep(0.1)
        self.redirect('/reg/leaderList')


class DeleteLeader(BaseHandler):

    def post(self):
        """Deletes leader from list"""
        lead_id = self.request.POST['idToDeleteChange']
        fio = self.request.POST['leadFio']
        db.delete(lead_id)
        time.sleep(0.1)
        global tooltip_message
        global tooltip_show
        tooltip_message = u'Руководитель %s удален из базы' % fio
        tooltip_show = 'block'
        self.redirect('/reg/leaderList')


class MembersHandler(BaseHandler):

    def get(self):
        """Diplays whole list of members"""
        user = users.get_current_user()
        if user:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            roles = OtherHandlers.create_roles_head(self, is_org, is_lead, is_memb)
            if is_org and self.session.get('role') == 'organizer':
                members = db.Query(Member).order('nickname')
                keys = []
                for memb in members:
                    keys.append(memb.key())
                global tooltip_message
                global tooltip_show
                tooltip_message = ''
                tooltip_show = 'none'
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'disp_tool': tooltip_show, 'tool': tooltip_message, 'members': members, 'keys': keys}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/MemberList.html')
                self.response.write(template.render(temp_values))
            else:
                show_unauth_page(self)
        else:
            show_unauth_page(self)

    def post(self):
        """Finds members by keyword"""
        user = users.get_current_user()
        if user:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            roles = OtherHandlers.create_roles_head(self, is_org, is_lead, is_memb)
            if is_org and self.session.get('role') == 'organizer':
                search_fio = self.request.POST['findMember']
                membs = db.Query(Member).filter('nickname >=', search_fio).filter('nickname <=', search_fio+'1')\
                            .order('nickname')
                keys = []
                for org in membs:
                    keys.append(org.key())
                global tooltip_message
                global tooltip_show
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'disp_tool': tooltip_show, 'tool': tooltip_message, 'members': membs, 'keys': keys}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/MemberList.html')
                self.response.write(template.render(temp_values))
            else:
                show_unauth_page(self)
        else:
            show_unauth_page(self)


class AddMember(BaseHandler):

    def post(self):
        """Changes existing member"""
        new_fio = self.request.POST['omFio']
        new_birthdate = self.request.POST['omGr']
        new_qual = self.request.POST['omRazr']
        new_command = self.request.POST['omComand']
        new_terry = self.request.POST['omTerritory']
        memb_key = self.request.POST['omKey']
        member = Member.get(memb_key)
        team = member.command
        team.name = new_command
        team.territory = new_terry
        team.put()
        member.nickname = new_fio
        member.birthdate = int(new_birthdate)
        member.qualification = new_qual
        member.command = team
        member.put()
        global tooltip_message
        global tooltip_show
        tooltip_message = u'Участник %s изменен' % new_fio
        tooltip_show = 'block'
        time.sleep(0.1)
        self.redirect('/reg/memberList')


class DeleteMember(BaseHandler):

    def post(self):
        """Deletes member from list"""
        self.response.write('1')
        memb_id = self.request.POST['idToDeleteChange']
        fio = self.request.POST['membFio']
        self.response.write('2')
        db.delete(memb_id)
        time.sleep(0.1)
        global tooltip_message
        global tooltip_show
        tooltip_message = u'Участник %s удален из базы' % fio
        tooltip_show = 'block'
        self.redirect('/reg/memberList')


