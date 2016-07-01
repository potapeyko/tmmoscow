# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
from google.appengine.api import users
from datetime import datetime
from google.appengine.ext import db


from modelCompetition import Competition
from modelVisitor import Organizer, Leader, Member, Command
from CompetitionHandlers import format_date_list
from LeaderHandlers import salt_pass
from Common import BaseHandler

__author__ = 'Daria'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class LoginHandler(BaseHandler):
    
    def get(self):
        """Displays login page"""
        user = users.get_current_user()
        if user:
            email = user.email()
            temp_values = {'user_email': email}
            template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/organizer/CompetitionList.html')
            self.response.write(template.render(temp_values))
        else:
            self.redirect(users.create_login_url(dest_url='/postSignIn'))


# Competition list
class DefaultHandler(BaseHandler):
    
    def get(self):
        """Displays list of competition"""
        try:
            loc_role = self.session.get('role')
        except:
            loc_role = 'anonim'
        comps = Competition.all().order('d_start')
        comps_count = comps.count()
        d_start = []
        d_finish = []
        pzs = []
        is_open_pz = []
        for c in comps:
            d_start.append(str(c.d_start))
            d_finish.append(str(c.d_finish))
            infos_of_comp = c.info_set.run(batch_size=1000)
            is_open = False
            for info_of_day in infos_of_comp:
                is_open = is_open or (info_of_day.pz_is_open and (datetime.today().date() < info_of_day.pz_add_end))
            is_open_pz.append(is_open)
        d_start = format_date_list(d_start)
        d_finish = format_date_list(d_finish)
        user = users.get_current_user()
        temp_values = {'comps': comps, 'c_count': comps_count, 'd_start': d_start, 'd_finish': d_finish, 'pzs': pzs,
                       'is_open_pz': is_open_pz}
        if not user:        # user is anonim
            login = users.create_login_url(dest_url='/postSignIn')
            temp_values.update({'login': login, 'is_user': True})
            template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/CompetitionList.html')
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = find_user(email)
            roles = create_roles_head(self, is_org, is_lead, is_memb)
            temp_values.update({'user_email': email, 'roles': roles, 'logout': users.create_logout_url('/login'), 
                                'is_user': True})
            try:            # show compList corresponding to user's role
                template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/%s/CompetitionList.html' % loc_role)
            except:         # user is anonim
                login = users.create_login_url(dest_url='/postSignIn')
                temp_values = {'login': login, 'comps': comps, 'c_count': comps_count, 'd_start': d_start, 'd_finish':
                            d_finish, 'pzs': pzs, 'is_open_pz': is_open_pz, 'logout': users.create_logout_url('/login')}
                template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/CompetitionList.html')
        self.response.write(template.render(temp_values))


class AfterSignIn(BaseHandler):
    
    def get(self):
        """Displays form for choosing current user role"""
        user = users.get_current_user()
        if not user:
            self.session['role'] = 'anonim'
            self.redirect('/')
        else:
            try:
                email = user.email()
                [is_org, is_lead, is_memb] = find_user(email)
                [roles, cur_role_local] = create_roles(is_org, is_lead, is_memb)
                if len(roles) > 1:      # If user has several roles, he should choose one
                    temp_values = {'roles': roles, 'logout': users.create_logout_url('/login')}
                    template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/AfterSignIn.html')
                    self.response.write(template.render(temp_values))
                else:                   # If user has only one role
                    self.session['role'] = cur_role_local
                    return webapp2.redirect('/')
            except:                                     # If user hasn't roles in system (anonim)
                self.session['role'] = 'anonim'
                self.redirect('/')

    def post(self):
        """Saves current user role"""
        cur_role_local = self.request.POST.get('curRole')
        self.session['role'] = cur_role_local
        self.redirect('/')


class beforeSignOut(BaseHandler):
    
    def get(self):
        """Throws out current role before signing out of system"""
        self.session['role'] = 'anonim'


class addDb(webapp2.RequestHandler):
    
    def get(self):
        """(for developing mode) Adds initial data to database"""
        user = users.get_current_user()
        com1 = Command(name=u'Фортуна', territory=u'Ангарск')
        com2 = Command(name=u'Командочка', territory=u'Москва')
        com1.put()
        com2.put()
        paswd = '123'
        paswd = salt_pass(paswd)
        org1 = Organizer(user=users.User('pro@m.c'), nickname=u'Провилкова Анна', contact='pro@m.c')
        org2 = Organizer(user=users.User('test@example.com'), nickname=u'Тест Тестович', contact='test@example.com')
        lead1 = Leader(user=users.User('pro@m.c'), nickname=u'Провилкова Анна', contact='pro@m.c', command=com1)
        lead2 = Leader(user=users.User('o@o.p'), nickname=u'Орлов Олег', contact='o@o.p', command=com1)
        lead3 = Leader(user=users.User('test@example.com'), nickname=u'Тест Тестович', contact='test@example.com', 
                       command=com2)
        memb1 = Member(pass_to_edit=paswd, sex=u'Женский', nickname='plo@m.r', surname=u'Плотникова Дарья', 
                       command=com1, birthdate=1994, qualification='I')
        memb2 = Member(pass_to_edit=paswd, sex=u'Мужской', nickname='mar@h.n', surname=u'Хайруллин Марат', command=com1,
                       birthdate=1994, qualification='I')
        memb3 = Member(pass_to_edit=paswd, sex=u'Мужской', nickname='pot@d.a', surname=u'Потапейко Дмитрий', 
                       command=com2, birthdate=1995, qualification='I')
        memb1.put()
        memb2.put()
        memb3.put()
        org1.put()
        org2.put()
        lead1.put()
        lead2.put()
        lead3.put()


def find_user(keyword):
    """Checks is user in database"""
    is_org = db.Query(Organizer).filter('contact =', keyword).count()
    is_lead = db.Query(Leader).filter('contact =', keyword).count()
    is_memb = db.Query(Member).filter('nickname =', keyword).count()
    return [is_org, is_lead, is_memb]


def create_roles_head(self, is_org, is_lead, is_memb):
    """Returns list of registered user roles for indicating available roles at page head"""
    roles = []
    if is_org:
        if self.session.get('role') == 'organizer':
            roles.append(u'<b>Организатор</b>')
        else:
            roles.append(u'Организатор')
    if is_lead:
        if self.session.get('role') == 'leader':
            roles.append(u'<b>Руководитель</b>')
        else:
            roles.append(u'Руководитель')
    if is_memb:
        if self.session.get('role') == 'member':
            roles.append(u'<b>Участник</b>')
        else:
            roles.append(u'Участник')
    return roles


def create_roles(is_org, is_lead, is_memb):
    """Returns list of registered user roles for choosing current role"""
    roles = []
    cur_role_local = 'anonim'
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


