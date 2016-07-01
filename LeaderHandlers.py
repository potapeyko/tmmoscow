# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
import random
import string
import hashlib
import time
from google.appengine.api import users
from google.appengine.ext import db

import OtherHandlers
from modelCompetition import DistInfo, Competition, Distance, CompMemb
from modelVisitor import Leader, Member
from Common import show_unauth_page, BaseHandler

__author__ = 'Daria'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Team(BaseHandler):

    def get(self):
        """Displays info about team and all members for current leader"""
        user = users.get_current_user()
        if not user:
            show_unauth_page(self)
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            roles = OtherHandlers.create_roles_head(self, is_org, is_lead, is_memb)
            if is_lead and self.session.get('role') == 'leader':
                leader = db.Query(Leader).filter('user =', user).get()
                team = leader.command
                territory = team.territory
                [membs, memb_keys] = membs_from_db(team)
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'team_name': team.name, 'terry': territory, 'membs': membs, 'membs_count': membs.count(),
                               'keys': memb_keys}
                template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/leader/Team.html')
                self.response.write(template.render(temp_values))
            else:
                show_unauth_page(self)

    def post(self):
        """Changes common info of team of current leader"""
        user = users.get_current_user()
        if not user:
            show_unauth_page(self)
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            if is_lead and self.session.get('role') == 'leader':
                new_name = self.request.POST.get('nameTeam')
                new_terry = self.request.POST.get('terryTeam')
                lead = db.Query(Leader).filter('user =', user).get()
                team = lead.command
                team.name = new_name
                team.territory = new_terry
                team.put()
                time.sleep(0.1)
                self.redirect('/reg/leaderTeam')
            else:
                show_unauth_page(self)


class AddMemberToTeam(BaseHandler):

    def get(self):
        """Displays empty form to add info about new member of current leader"""
        user = users.get_current_user()
        if not user:
            show_unauth_page(self)
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            roles = OtherHandlers.create_roles_head(self, is_org, is_lead, is_memb)
            if is_lead and self.session.get('role') == 'leader':
                pass_to_edit = generate_pass()
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'edit_pass': pass_to_edit, 'card_title': u'Новый участник команды', 'new_memb': True}
                template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/leader/Member.html')
                self.response.write(template.render(temp_values))
            else:
                show_unauth_page(self)

    def post(self):
        """Saves info about new member of current leader"""
        user = users.get_current_user()
        if not user:
            show_unauth_page(self)
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            if is_lead and self.session.get('role') == 'leader':
                member = save_member_from_post(self)
                member.pass_to_edit = salt_pass(self.request.POST.get('passToEdit'))
                member.command = db.Query(Leader).filter('user =', user).get().command
                member.put()
                time.sleep(0.1)
                self.redirect('/reg/leaderTeam')
            else:
                show_unauth_page(self)


class ChangeMember(BaseHandler):

    def get(self):
        """Displays form to change info about member of current leader"""
        user = users.get_current_user()
        if not user:
            show_unauth_page(self)
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            roles = OtherHandlers.create_roles_head(self, is_org, is_lead, is_memb)
            if is_lead and self.session.get('role') == 'leader':
                memb_key = self.request.get('change')
                member = db.get(memb_key)
                [sex_m, sex_w] = check_sex(member)
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'card_title': u'Изменение участника', 'memb_name':
                                   member.surname, 'birthdate': member.birthdate, 'qual': member.qualification, 'sex_m':
                                   sex_m, 'sex_w': sex_w, 'new_memb': False, 'memb_key': memb_key, 'change': memb_key}
                template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/leader/Member.html')
                self.response.write(template.render(temp_values))
            else:
                show_unauth_page(self)

    def post(self):
        """Saves changes about member of current leader"""
        user = users.get_current_user()
        if not user:
            show_unauth_page(self)
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            if is_lead and self.session.get('role') == 'leader':
                memb_key = self.request.POST.get('change')
                member = db.get(memb_key)

                save_member_from_post(self, member)
                time.sleep(0.1)
                self.redirect('/reg/leaderTeam')
            else:
                show_unauth_page(self)


class DeleteMember(BaseHandler):

    def post(self):
        """Deletes chosen member of current leader"""
        user = users.get_current_user()
        if not user:
            show_unauth_page(self)
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            if is_lead and self.session.get('role') == 'leader':
                memb_key = self.request.POST.get('delete')
                db.delete(memb_key)
                time.sleep(0.1)
                self.redirect('/reg/leaderTeam')
            else:
                show_unauth_page(self)


class EntryMembers(BaseHandler):

    def get(self):
        """Displays list of team members to mark some on current competition"""
        user = users.get_current_user()
        if not user:
            show_unauth_page(self)
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            roles = OtherHandlers.create_roles_head(self, is_org, is_lead, is_memb)
            if is_lead and self.session.get('role') == 'leader':
                comp_key = self.request.GET['competition']
                competition = Competition.get(comp_key)
                leader = db.Query(Leader).filter('user =', user).get()
                team = leader.command
                team_q = db.Query(Member).filter('command =', team).order('surname')
                memb_team = team_q.run(batch_size=1000)
                entry_membs = []
                no_entry_membs = []
                days = []
                for memb in memb_team:
                    m = db.Query(CompMemb).filter('competition =', competition).filter('member =', memb)
                    membs = m.run()
                    if m.count():
                        entry_membs.append(memb)
                        m_d = []
                        for mem in membs:
                            m_d.append(mem.day_numb)
                        days.append(m_d)
                    else:
                        no_entry_membs.append(memb)
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'team_name': team.name, 'membs_count': team_q.count(), 'entry_membs': entry_membs,
                               'no_entry_membs': no_entry_membs, 'comp_name': competition.name, 'days_count':
                                   range(1, int(competition.days_count) + 1), 'comp_key': comp_key, 'days': days}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/leader/MembersToCompetition.html')
                self.response.write(template.render(temp_values))
            else:
                show_unauth_page(self)


class EntryMembersByDay(BaseHandler):

    def post(self):
        """Displays members added to current competition to check their groups"""
        user = users.get_current_user()
        if not user:
            show_unauth_page(self)
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            roles = OtherHandlers.create_roles_head(self, is_org, is_lead, is_memb)
            if is_lead and self.session.get('role') == 'leader':
                comp_key = self.request.POST.get('competition')
                competition = Competition.get(comp_key)
                days_count = competition.days_count
                membs_by_day = []
                show_tables = False
                for i in range(days_count):  # add members (keys) for each day
                    membs_key_day = self.request.POST.getall('checkMemb' + str(i))
                    membs_i_day = []
                    for memb_key in membs_key_day:
                        member = Member.get(memb_key)
                        membs_i_day.append(member)
                        if show_tables == False: show_tables = True
                    membs_by_day.append(membs_i_day)

                dist_query = db.Query(Distance).filter('competition =', competition)
                distances = dist_query.run()
                type_lent = []
                groups_on_day = []
                for dist in distances:
                    type_lent.append(dist.type + ' ' + dist.lent)
                    dist_infos = dist.distinfo_set.run(batch_size=1000)
                    groups_i_day = []
                    for info in dist_infos:
                        groups_i_day.append(info.group_name)
                    groups_on_day.append(groups_i_day)
                temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/login'),
                               'membs_by_day': membs_by_day, 'dists': type_lent, 'groups': groups_on_day, 'comp_key':
                                   comp_key, 'show_tables': show_tables}
                template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/leader/MembersToDays.html')
                self.response.write(template.render(temp_values))
            else:
                show_unauth_page(self)


class AcceptMembers(BaseHandler):

    def post(self):
        """Saves members that will take a part in competition to database"""
        user = users.get_current_user()
        if not user:
            show_unauth_page(self)
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = OtherHandlers.find_user(email)
            if is_lead and self.session.get('role') == 'leader':
                days_checked_count = int(self.request.POST.get('daysCheckedCount'))
                comp_key = self.request.POST.get('competition')
                competition = Competition.get(comp_key)
                dist_query = db.Query(Distance).filter('competition =', competition)
                distances = dist_query.run(batch_size=1000)
                distinfos = []                                  # all groups of all days
                for dist in distances:
                    distinfo = db.Query(DistInfo).filter('distance =', dist).run()          # all groups for that day (=distance)
                    distinfos.append(distinfo)
                for i_day in range(days_checked_count):         # runs through all days one by one
                    memb_count_i_day = int(self.request.POST.get('membsInDay%s' % str(i_day)))
                    for j_memb in range(memb_count_i_day):       # runs through all member of i- day
                        memb_group = self.request.POST.get('checkMembGroup%s' % str(i_day)+'_%s' % str(j_memb))
                        keys = memb_group.split('_')
                        member = Member.get(keys[0])
                        group_code = keys[1]
                        CompMemb(competition=competition, member=member, group=group_code, day_numb=i_day+1).put()
                time.sleep(0.1)
                self.redirect('/competition?dbKey=%s' % comp_key)
            else:
                show_unauth_page(self)


def generate_pass():
    """Generates 8-symbol password"""
    rid = ''
    for x in range(8):
        rid += random.choice(string.ascii_letters + string.digits)
    return rid


def salt_pass(paswd):
    """Salts user's password"""
    md = hashlib.md5()
    md.update(paswd)
    md.update('dado')       # This is salt
    return md.hexdigest()


def check_sex(member):
    """Converts member's sex to 'checked' state of checkbox"""
    sex_m = ''
    sex_w = ''
    if member.sex == u'Мужской':
        sex_m = 'checked'
    else:
        sex_w = 'checked'
    return [sex_m, sex_w]


def membs_from_db(team):
    """Gets all members of current team from database"""
    membs = db.Query(Member).filter('command =', team).order('surname')
    memb_keys = []
    for memb in membs:
        memb_keys.append(memb.key())
    return [membs, memb_keys]


def save_member_from_post(self, existed_memb=None):
    """Saves new data or changes to current member in database"""
    if not existed_memb:     # get new member
        surname = self.request.POST.get('surnameMemb')
        birthdate = int(self.request.POST.get('birthdate'))
        qual = self.request.POST.get('qualMemb')
        sex = self.request.POST.get('sexMemb')
        return Member(surname=surname, birthdate=birthdate, qualification=qual, sex=sex)
    else:               # change member
        existed_memb.surname = self.request.POST.get('surnameMemb')
        existed_memb.birthdate = int(self.request.POST.get('birthdate'))
        existed_memb.qualification = self.request.POST.get('qualMemb')
        existed_memb.sex = self.request.POST.get('sexMemb')
        existed_memb.put()
