# -*- coding: utf-8 -*-
__author__ = 'Daria'

from google.appengine.api import users
import os
import jinja2
import webapp2
import time

from modelVisitor import *
from OtherHandlers import cur_role


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

tooltip_message = ''
tooltip_show = 'none'


class OrganizersHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email = user.email()
            orgs = db.Query(Organizer).order('nickname')
            keys = []
            for org in orgs:
                keys.append(org.key())
            global tooltip_message
            global tooltip_show
            temp_values = {'user_email':email, 'logout':users.create_logout_url('/login'), 'disp_tool':tooltip_show, 'tool':tooltip_message, 'organizers':orgs, 'keys':keys}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/OrganizerList.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = {'img_src':'../static/img/er401.png', 'er_name':'401', 'login_redir':users.create_login_url('reg/organizerList')}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))

    def post(self):
        user = users.get_current_user()
        if user:
            email = user.email()
            search_fio = self.request.POST['findOrganizer']
            orgs = db.Query(Organizer).filter('nickname >=', search_fio).filter('nickname <=', search_fio+'1').order('nickname')
            keys = []
            for org in orgs:
                keys.append(org.key())
            global tooltip_message
            global tooltip_show
            temp_values = {'user_email':email, 'logout':users.create_logout_url('/login'), 'disp_tool':tooltip_show, 'tool':tooltip_message, 'organizers':orgs, 'keys':keys}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/OrganizerList.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = {'img_src':'../static/img/er401.png', 'er_name':'401', 'login_redir':users.create_login_url('reg/organizerList')}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))


class AddOrganizer(webapp2.RequestHandler):
    def post(self):
        if self.request.POST['olKey']:  #changing existing organizer
            new_fio = self.request.POST['olFio']
            new_contact = self.request.POST['olContact']
            org_key = self.request.POST['olKey']
            organizer = Organizer.get(org_key)
            organizer.nickname = new_fio
            organizer.contact = new_contact
            organizer.put()
            tooltip_message = u'Организатор %s изменен' % new_fio
        else:   #add new organizer
            fio = self.request.POST['olFio']
            contact = self.request.POST['olContact']
            newOrg = Organizer(nickname=fio, contact=contact)
            newOrg.put()
            global tooltip_message
            global tooltip_show
            tooltip_message = u'Организатор %s добавлен базу' % fio
        tooltip_show = 'block'
        time.sleep(0.1)
        self.redirect('/reg/organizerList')


class DeleteOrganizer(webapp2.RequestHandler):
    def post(self):
        org_id = self.request.POST['idToDeleteChange']
        fio = self.request.POST['organFio']
        db.delete(org_id)
        time.sleep(0.1)
        global tooltip_message
        global tooltip_show
        tooltip_message = u'Организатор %s удален из базы' % fio
        tooltip_show = 'block'
        self.redirect('/reg/organizerList')


class LeadersHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email = user.email()
            leads = db.Query(Leader).order('nickname')
            keys = []
            for lead in leads:
                keys.append(lead.key())
            global tooltip_message
            global tooltip_show
            temp_values = {'user_email':email, 'logout':users.create_logout_url('/login'), 'disp_tool':tooltip_show, 'tool':tooltip_message, 'leads':leads, 'keys':keys}
            tooltip_message = ''
            tooltip_show = 'none'
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/LeaderList.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = {'img_src':'../static/img/er401.png', 'er_name':'401', 'login_redir':users.create_login_url('reg/leaderList')}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))

    def post(self):
        user = users.get_current_user()
        if user:
            email = user.email()
            search_fio = self.request.POST['findLeader']
            leads = db.Query(Leader).filter('nickname >=', search_fio).filter('nickname <=', search_fio+'1').order('nickname')
            keys = []
            for org in leads:
                keys.append(org.key())
            global tooltip_message
            global tooltip_show
            temp_values = {'user_email':email, 'logout':users.create_logout_url('/login'), 'disp_tool':tooltip_show, 'tool':tooltip_message, 'leads':leads, 'keys':keys}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/LeaderList.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = {'img_src':'../static/img/er401.png', 'er_name':'401', 'login_redir':users.create_login_url('reg/organizerList')}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))


class AddLeader(webapp2.RequestHandler):
    def post(self):
        if self.request.POST['llKey']:  #changing existing leader
            new_fio = self.request.POST['llFio']
            new_command = self.request.POST['llComand']
            new_terry = self.request.POST['llTerritory']
            new_contact = self.request.POST['llContact']
            lead_key = self.request.POST['llKey']
            leader = Leader.get(lead_key)
            leader.nickname = new_fio
            leader.command = new_command
            leader.territory = new_terry
            leader.contact = new_contact
            leader.put()
            tooltip_message = u'Руководитель %s изменен' % new_fio
        else:   #add new leader
            fio = self.request.POST['llFio']
            command = self.request.POST['llComand']
            terry = self.request.POST['llTerritory']
            contact = self.request.POST['llContact']
            newLead = Leader(nickname=fio, command=command, territory=terry, contact=contact)
            newLead.put()
            global tooltip_message
            global tooltip_show
            tooltip_message = u'Руководитель %s добавлен базу' % fio
        tooltip_show = 'block'
        time.sleep(0.1)
        self.redirect('/reg/leaderList')


class DeleteLeader(webapp2.RequestHandler):
    def post(self):
        lead_id = self.request.POST['idToDeleteChange']
        fio = self.request.POST['leadFio']
        db.delete(lead_id)
        time.sleep(0.1)
        global tooltip_message
        global tooltip_show
        tooltip_message = u'Руководитель %s удален из базы' % fio
        tooltip_show = 'block'
        self.redirect('/reg/leaderList')


class MembersHandler(webapp2.RequestHandler):   # shows list of all members from datastore
    def get(self):
        user = users.get_current_user()
        if user:
            email = user.email()
            members = db.Query(Member).order('nickname')
            keys = []
            for memb in members:
                keys.append(memb.key())
            global tooltip_message
            global tooltip_show
            temp_values = {'user_email':email, 'logout':users.create_logout_url('/login'), 'disp_tool':tooltip_show, 'tool':tooltip_message, 'members':members, 'keys':keys}
            tooltip_message = ''
            tooltip_show = 'none'
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/MemberList.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = {'img_src':'../static/img/er401.png', 'er_name':'401', 'login_redir':users.create_login_url('reg/memberList')}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))

    def post(self):
        user = users.get_current_user()
        if user:
            email = user.email()
            search_fio = self.request.POST['findMember']
            membs = db.Query(Member).filter('nickname >=', search_fio).filter('nickname <=', search_fio+'1').order('nickname')
            keys = []
            for org in membs:
                keys.append(org.key())
            global tooltip_message
            global tooltip_show
            temp_values = {'user_email':email, 'logout':users.create_logout_url('/login'), 'disp_tool':tooltip_show, 'tool':tooltip_message, 'members':membs, 'keys':keys}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/MemberList.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = {'img_src':'../static/img/er401.png', 'er_name':'401', 'login_redir':users.create_login_url('reg/organizerList')}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))


class AddMember(webapp2.RequestHandler):
    def post(self):
        cur_user = users.get_current_user()
        leader = db.Query(Leader).filter('user =', cur_user).get()
        if self.request.POST['omKey']:  # change existing member
            new_fio = self.request.POST['omFio']
            new_birthdate = self.request.POST['omGr']
            new_qual = self.request.POST['omRazr']
            new_command = self.request.POST['omComand']
            new_terry = self.request.POST['omTerritory']
            memb_key = self.request.POST['omKey']
            member = Member.get(memb_key)
            member.nickname = new_fio
            member.command = new_command
            member.territory = new_terry
            member.birthdate = int(new_birthdate)
            member.qualification = new_qual
            member.put()
            tooltip_message = u'Участник %s изменен' % new_fio
        else:   #add new member
            fio = self.request.POST['omFio']
            bdate = int(self.request.POST['omGr'])
            qual = self.request.POST['omRazr']
            comm = self.request.POST['omComand']
            terr = self.request.POST['omTerritory']
            newMember = Member(nickname=fio, birthdate=bdate, qualification=qual, leader=leader, command=comm, territory=terr)
            newMember.put()
            global tooltip_message
            global tooltip_show
            tooltip_message = u'Участник %s добавлен базу' % fio
        tooltip_show = 'block'
        time.sleep(0.1)
        self.redirect('/reg/memberList')


class DeleteMember(webapp2.RequestHandler):
    def post(self):
        memb_id = self.request.POST['idToDeleteChange']
        fio = self.request.POST['membFio']
        db.delete(memb_id)
        time.sleep(0.1)
        global tooltip_message
        global tooltip_show
        tooltip_message = u'Участник %s удален из базы' % fio
        tooltip_show = 'block'
        self.redirect('/reg/memberList')


