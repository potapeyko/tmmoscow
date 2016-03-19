# -*- coding: utf-8 -*-
__author__ = 'Daria'

from google.appengine.api import users
from google.appengine.api import images
import os
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class NewCompetitionInfo(webapp2.RequestHandler):
    def get(self):  # shows empty form for adding new competition's common info
        user = users.get_current_user()
        if user:
            email = user.email()
            temp_values = {'user_email': email, 'logout': users.create_logout_url('/login')}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/NewCompetitionInfo.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                           'login_redir': users.create_login_url('/reg/newCompetition')}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))

    def post(self):  # save filled form about new competition
        user = users.get_current_user()
        if user:
            email = user.email()
            temp_values = {'user_email': email, 'logout': users.create_logout_url('/login')}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/NewCompetitionInfo.html')
            self.response.write(template.render(temp_values))


class NewCompetition(webapp2.RequestHandler):
    def get(self):  # shows empty form for adding new competition
        user = users.get_current_user()
        if user:
            email = user.email()
            name = self.request.GET['nameCompNew']
            d_s = self.request.GET['dateStartNew']
            d_f = self.request.GET['dateFinishNew']
            d_count = self.request.GET['countStart']
            try:
                write_places = self.request.GET['checkPlaces']
                write_places = True
            except:
                write_places = False
            try:
                show_map = self.request.GET['checkPlacesMap']
                show_map = True
            except:
                show_map = False
            temp_values = {'user_email': email, 'logout': users.create_logout_url('/login'), 'd_start': formatDate(d_s),
                           'd_finish': formatDate(d_f), 'name': name, 'days_count': range(1, int(d_count) + 1),
                           'write_places': write_places, 'show_map': show_map, 'd_count': d_count}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/AddCompetition.html', )
            self.response.write(template.render(temp_values))
        else:
            temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                           'login_redir': users.create_login_url('/reg/addCompetition')}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))

    def post(self):  # save filled form about new competition
        user = users.get_current_user()
        if user:
            email = user.email()
            # common info about competition
            start_date = self.request.POST['dateStartNew']
            finish_date = self.request.POST['dateFinishNew']
            comp_name = self.request.POST['nameCompNew']
            d_count = self.request.POST['dayCount']
            show_places = self.request.POST['writePlaces']
            show_map = self.request.POST['showMap']

            # info tab
            pz_end_add = formatDateList(self.request.POST.getall('pzEndAddNew'))
            pz_end_change = formatDateList(self.request.POST.getall('pzEndChangeNew'))
            links = self.request.POST.getall('toTmMoscowNew')
            places = self.request.POST.getall('placeNew')
            pzs = []
            tzs = []
            orgs = []
            org_fios = []; org_dols = []; org_conts=[];
            for i in range(1, int(d_count)+1):
                #org_fios = []; org_dols = []; org_conts=[];
                pzs.append(self.request.POST.getall('trPzNew'+str(i)))
                tzs.append(self.request.POST.getall('trTzNew'+str(i)))
                org_fios.append(self.request.POST.getall('orgFioNew'+str(i)))
                org_dols.append(self.request.POST.getall('orgDolNew'+str(i)))
                org_conts.append(self.request.POST.getall('orgContNew'+str(i)))
            for i in range(int(d_count)):
                orgs.append(zip(org_fios[i], org_dols[i], org_conts[i]))
            pzs = onToChecked(pzs)
            tzs = onToChecked(tzs)

            # diz tab
            disciplines = []
            for i in range(1, int(d_count)+1):
                disciplines.append(self.request.POST['dizDisciplineNew'+str(i)])
            disciplines = convertToDiscString(disciplines)


            temp_values = {'user_email': email, 'logout': users.create_logout_url('/login'), 'start': start_date,
                           'finish': finish_date, 'name': comp_name, 'show_places': show_places, 'show_map': show_map,
                           'days_count': range(1, int(d_count) + 1), 'pz_end_add': pz_end_add, 'pz_end_change':
                           pz_end_change, 'links': links, 'places': places, 'pzs': pzs, 'tzs': tzs, 'org_infos': orgs,
                           'discs': disciplines}
            # zip(org_fios, org_dols, org_conts)

            # , 'count_start':count_start, 'start_places':start_places,
            # 'pzs':pz, 'pzEndAdds':pz_end_add, 'pzEndChanges':pz_end_change, 'tzs':tz, 'links':link_to_tmmosc,
            # 'orgs': org_info}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/Competition.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401',
                           'login_redir': users.create_login_url('/reg/newCompetition')}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))

    def getClientCompInfo(self):
        pass

    def getCientDizInfo(self):
        pass

    def getClientStatistic(self):
        pass


class CertainCompetition(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            email = 'Anonymous'
            role = 'Anonim'
        else:
            email = user.email()
            role = user.nickname()
        temp_values = {'user_email': email, 'logout': users.create_logout_url('/login')}
        template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/Competition.html')
        self.response.write(template.render(temp_values))

    def post(self):
        self.response.write('POST Add new info about competition (ORG)')


def formatDate(bad_date):
    ymd = bad_date.split('-')
    y = ymd[0]
    m = ymd[1]
    d = ymd[2]
    return str(d) + '.' + str(m) + '.' + str(y)

def formatDateList(bad_date_list):
    good_dates = []
    for date in bad_date_list:
        good_dates.append(formatDate(date))
    return good_dates

def dayNumbers(count):
    days = []
    for i in range(0, count):
        days.append(i)
    return days

def onToChecked(check_list):
    checked_list = []
    for check in check_list:
        if str(check).find('on') > 0:
            checked_list.append('checked')
        else:
            checked_list.append('')
    return checked_list

def convertToDiscString(disciplines):
    stringDiscs = []
    for discipline in disciplines:
        if discipline == '1':
            stringDiscs.append(u'Пешеходная')
            continue
        if discipline == '2':
            stringDiscs.append(u'Пешеходная-связка')
            continue
        if discipline == '3':
            stringDiscs.append(u'Пешеходная-группа')
            continue
    return stringDiscs