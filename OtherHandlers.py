# -*- coding: utf-8 -*-
__author__ = 'Daria'

from google.appengine.api import users
from datetime import datetime
import os
import jinja2
import webapp2
from google.appengine.ext import db
from modelCompetition import Competition, Info, MemInfo, DistInfo, Distance
from modelVisitor import Organizer, Leader, Member
from CompetitionHandlers import formatDateList

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

cur_role = 'member'

# LogIn page
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email = user.email()
            temp_values = {'user_email': email}
            template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/organizer/CompetitionList.html')
            self.response.write(template.render(temp_values))
        else:
            self.redirect(users.create_login_url(dest_url='/postSignIn'))
      #  temp_values = {}
      #  template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/LogIn.html')
      #  self.response.write(template.render(temp_values))

    def post(self):
        self.response.write('POST Registration of user')


# Competition list
class DefaultHandler(webapp2.RequestHandler):
    def get(self):
        global cur_role
        comps = Competition.all().order('d_start')
        comps_count = comps.count()
        d_start = [];
        d_finish = [];
        pzs = [];
        is_open_pz = []
        for c in comps:
            d_start.append(str(c.d_start))
            d_finish.append(str(c.d_finish))
            infos_of_comp = c.info_set.run(batch_size=1000)  # Returns one or several Info objects (instance or list)
            is_open = False
            for info_of_day in infos_of_comp:
                is_open = is_open or (info_of_day.pz_is_open and (datetime.today().date() < info_of_day.pz_add_end))
            is_open_pz.append(is_open)
        d_start = formatDateList(d_start)
        d_finish = formatDateList(d_finish)
        user = users.get_current_user()
        if not user:
            email = 'Anonymous'
            role = 'Anonim'
            login = users.create_login_url(dest_url='/postSignIn')
            temp_values = {'login': login, 'comps': comps, 'c_count': comps_count, 'd_start': d_start,
                           'd_finish': d_finish, 'pzs': pzs, 'is_open_pz': is_open_pz, 'is_user': False,
                           'logout': users.create_logout_url('/login')}
            template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/member/CompetitionList.html')
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = findUser(email)
            roles = createRolesHead(is_org, is_lead, is_memb)
            temp_values = {'user_email': email, 'roles': roles, 'logout': users.create_logout_url('/login'), 'comps': comps,
                           'c_count': comps_count, 'd_start': d_start, 'd_finish': d_finish, 'pzs': pzs, 'is_open_pz': is_open_pz,
                           'cur_role': cur_role}
            try:
                template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/'+cur_role+'/CompetitionList.html')
            except:
                temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                               'login_redir': users.create_login_url('/reg/newCompetition')}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html')
        self.response.write(template.render(temp_values))


class AfterSignIn(webapp2.RequestHandler):
    def get(self):      # displays form for choosing current user role
        user = users.get_current_user()
        email = user.email()
        [is_org, is_lead, is_memb] = findUser(email)
        [roles, cur_role_local] = createRoles(is_org, is_lead, is_memb)
        if len(roles) > 1:   # If user has several roles, he should choose one
            temp_values = {'roles': roles, 'logout': users.create_logout_url('/login') }
            template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/AfterSignIn.html')
            self.response.write(template.render(temp_values))
        else:                   # If user has only one role
            global cur_role
            cur_role = cur_role_local
            return webapp2.redirect('/')

    def post(self):     # changes current role to user's choice
        cur_role_local = self.request.POST.get('curRole')
        global cur_role
        cur_role = cur_role_local
        return webapp2.redirect('/')


# Zeros out current role to 'member' before sign out of system
class beforeSignOut(webapp2.RequestHandler):
    def get(self):
        global cur_role
        cur_role = 'member'


# Finds user in database
def findUser(keyword):
    is_org = db.Query(Organizer).filter('contact =', keyword).count()
    is_lead = db.Query(Leader).filter('contact =', keyword).count()
    is_memb = db.Query(Member).filter('nickname =', keyword).count()
    return [is_org, is_lead, is_memb]

# Returns list of registered user roles for indicating available roles at page head
def createRolesHead(is_org, is_lead, is_memb):
    roles = []
    if is_org:
        if cur_role == 'organizer':
            roles.append(u'<b>Организатор</b>')
        else:
            roles.append(u'Организатор')
    if is_lead:
        if cur_role == 'leader':
            roles.append(u'<b>Руководитель</b>')
        else:
            roles.append(u'Руководитель')
    if is_memb:
        if cur_role == 'member':
            roles.append(u'<b>Участник</b>')
        else:
            roles.append(u'Участник')
    return roles

# Returns list of registered user roles for choosing current role
def createRoles(is_org, is_lead, is_memb):
    roles = []
    if is_org:
        roles.append(u'Организатор соревнований')
        cur_role_local = 'organizer'
    if is_lead:
        roles.append(u'Руководитель команды')
        cur_role_local = 'leader'
    if is_memb:
        roles.append(u'Участник соревнований')
        cur_role_local = 'member'
    return [roles, cur_role_local]


