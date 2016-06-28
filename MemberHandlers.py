# -*- coding: utf-8 -*-

from google.appengine.api import users
import os
import jinja2
import webapp2
import time
from google.appengine.ext import db
from modelVisitor import Member
from modelCompetition import Competition, CompMemb, Distance, DistInfo
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

    def post(self):     # saves member's changes
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
        keys_in_comp = []
        keys_not_in = []
        memb_not_in = []
        memb_in_comp = []
        membs_comps = db.Query(CompMemb).filter('competition =', comp).order('member').run(batch_size=10000)
        for m in membs_comps:
            if m.member.key() not in keys_in_comp:
                memb_in_comp.append(m.member)
                keys_in_comp.append(m.member.key())
        for m in membs:
            if m.key() not in keys_in_comp:
                keys_not_in.append(m.key())
                memb_not_in.append(m)
        temp_values = {'login': login, 'logout': users.create_logout_url('/login'), 'name': comp.name, 'membs_count':
                       membs.count(), 'membs_in': memb_in_comp, 'membs_not': memb_not_in, 'keys_in': keys_in_comp,
                       'keys_not': keys_not_in, 'competition': comp_key}
        template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/member/MemberList.html')
        self.response.write(template.render(temp_values))


class AddMembToGroup(webapp2.RequestHandler):       # displays competition's groups by days to check member
    def post(self):
        login = users.create_login_url(dest_url='/postSignIn')
        memb_key = self.request.POST.get('member')
        memb = Member.get(memb_key)
        comp_key = self.request.POST.get('competition')
        comp = Competition.get(comp_key)
        distances = db.Query(Distance).filter('competition =', comp).order('day_numb')
        groups_by_days = []
        for dist in distances:
            groups_by_days.append(dist.distinfo_set.run(batch_size=100))
        temp_values = {'login': login, 'logout': users.create_logout_url('/login'), 'name': comp.name, 'surname':
                        memb.surname, 'team': memb.command.name, 'memb_key': memb_key, 'competition': comp_key,
                       'card_title': u'Заявка участника', 'dists': distances, 'groups_by_day': groups_by_days}
        template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/member/ToDaysGroups.html')
        self.response.write(template.render(temp_values))


class EnterMember(webapp2.RequestHandler):
    def post(self):
        memb_key = self.request.POST.get('member')
        memb = Member.get(memb_key)
        paswd = self.request.POST.get('changePass')
        comp_key = self.request.POST.get('competition')
        comp = Competition.get(comp_key)
        if saltPass(paswd) == memb.pass_to_edit:
            for i in range(comp.days_count):
                infos_count = int(self.request.POST.get('infosCount'+str(i)))
                for group_num in range(infos_count):
                    checked_group = self.request.POST.get('checkMembGroup'+str(i)+str(group_num))
                    if checked_group:
                        entry = CompMemb(competition=comp, member=memb, group=checked_group, day_numb=i+1)
                        entry.save()
                        time.sleep(0.1)
                        self.redirect('/entryOneMemb?competition=' + comp_key)
        else:
            login = users.create_login_url(dest_url='/postSignIn')
            distances = db.Query(Distance).filter('competition =', comp).order('day_numb')
            groups_by_days = []
            for dist in distances:
                groups_by_days.append(dist.distinfo_set.run(batch_size=100))
            temp_values = {'login': login, 'logout': users.create_logout_url('/login'), 'name': comp.name, 'surname':
                            memb.surname, 'team': memb.command.name, 'memb_key': memb_key, 'competition': comp_key,
                           'card_title': u'Заявка участника', 'dists': distances, 'groups_by_day': groups_by_days,
                           'tooltip': u'Неверный пароль подтверждения. Попробуйте еще раз'}
            template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/member/ToDaysGroups.html')
            self.response.write(template.render(temp_values))

class DeleteMemberFromComp(webapp2.RequestHandler):
    def get(self):      # displays form to fill in pass_to_edit
        login = users.create_login_url(dest_url='/postSignIn')
        comp_key = self.request.GET['competition']
        memb_key = self.request.GET['member']
        comp = Competition.get(comp_key)
        member = Member.get(memb_key)
        temp_values = {'login': login, 'logout': users.create_logout_url('/login'), 'name': comp.name, 'competition':
                        comp_key, 'memb_key': memb_key, 'surname': member.surname, 'team': member.command.name,
                       'card_title': u'Удаление участника из заявки'}
        template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/member/EnterPass.html')
        self.response.write(template.render(temp_values))

    def post(self):     # deletes member from that competition
        login = users.create_login_url(dest_url='/postSignIn')
        memb_key = self.request.POST.get('member')
        member = Member.get(memb_key)
        paswd = self.request.POST.get('changePass')
        comp_key = self.request.POST.get('competition')
        comp = Competition.get(comp_key)
        if saltPass(paswd) == member.pass_to_edit:
            comp_membs = CompMemb.all().filter('member =', member).filter('competition =', comp)
            db.delete(comp_membs)
            time.sleep(0.1)
            self.redirect('/entryOneMemb?competition=' + comp_key)
        else:
            temp_values = {'login': login, 'logout': users.create_logout_url('/login'), 'name': comp.name, 'surname':
                           member.surname, 'team': member.command.name, 'competition': comp_key, 'memb_key': memb_key,
                           'tooltip': u'Неверный пароль подтверждения. Попробуйте еще раз', 'card_title':
                            u'Удаление участника из заявки'}
            template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/member/EnterPass.html')
            self.response.write(template.render(temp_values))
