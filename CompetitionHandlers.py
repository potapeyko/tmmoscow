# -*- coding: utf-8 -*-
__author__ = 'Daria'

from google.appengine.api import users
from datetime import date
from google.appengine.api import images
from modelCompetition import MemInfo, DistInfo, Competition, Distance, Info
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

    def post(self):  # ??? save filled form about new competition
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
            write_places = readCheckboxGet(self, 'checkPlaces')
            show_map = readCheckboxGet(self, 'checkPlacesMap')

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
            d_count = int(self.request.POST['dayCount'])
            show_places = self.request.POST['writePlaces']
            show_map = self.request.POST['showMap']

            # statistic tab
            stat_day = readCheckboxPost(self, 'statistic0')
            stat_sex = readCheckboxPost(self, 'statistic1')
            stat_qual = readCheckboxPost(self, 'statistic2')

            competition = Competition(name=comp_name, d_start=dateToPython(start_date),
                                      d_finish=dateToPython(finish_date), days_count=d_count, places=["place1"],
                                      statistic=[stat_day, stat_sex, stat_qual])
            competition.save()

            # info tab
            pz_end_add = formatDateList(self.request.POST.getall('pzEndAddNew'))
            pz_end_change = formatDateList(self.request.POST.getall('pzEndChangeNew'))
            links = self.request.POST.getall('toTmMoscowNew')
            places = self.request.POST.getall('placeNew')
            pzs = []
            tzs = []
            orgs = []
            org_fios = []; org_dols = []; org_conts=[];
            for i in range(1, d_count+1):
                pzs.append(self.request.POST.getall('trPzNew'+str(i)))
                tzs.append(self.request.POST.getall('trTzNew'+str(i)))
                org_fios.append(self.request.POST.getall('orgFioNew'+str(i)))
                org_dols.append(self.request.POST.getall('orgDolNew'+str(i)))
                org_conts.append(self.request.POST.getall('orgContNew'+str(i)))
            for i in range(d_count):
                one_day_orgs = zip(org_fios[i], org_dols[i], org_conts[i])
                orgs.append(one_day_orgs)
                info = Info(competition=competition, day_numb=i, place_addr=places[i],
                            pz_is_open=onToBoolean(pzs[i]), pz_add_end=dateToPython(pz_end_add[i]),
                            pz_change_end=dateToPython(pz_end_change[i]), tz_is_on=onToBoolean(tzs[i]),
                            link=links[i], orgs=['orgs'])
                info.save()
            pzs = onToChecked(pzs)
            tzs = onToChecked(tzs)

            # diz tab
            disciplines = []
            lengths = []
            dizs = []
            dus = []
            diz_groups = []; diz_length = []; diz_class = []; diz_min_com = []; diz_max_com = [];
            du_group = []; du_salary = []; du_age_min = []; du_age_max = []; du_qual_min = []; du_qual_max = [];
            for i in range(1, d_count+1):
                disciplines.append(self.request.POST['dizDisciplineNew'+str(i)])
                lengths.append(self.request.POST['dizLengthNew'+str(i)])
                diz_groups.append(self.request.POST.getall('dizGroupNew'+str(i)))
                diz_length.append(self.request.POST.getall('dizLenNew'+str(i)))
                diz_class.append(self.request.POST.getall('dizClassNew'+str(i)))
                diz_min_com.append(self.request.POST.getall('dizCCminNew'+str(i)))
                diz_max_com.append(self.request.POST.getall('dizCCmaxNew'+str(i)))
                du_group.append(self.request.POST.getall('duGroupNew'+str(i)))
                du_salary.append(self.request.POST.getall('duSalaryNew'+str(i)))
                du_age_min.append(self.request.POST.getall('duAgeminNew'+str(i)))
                du_age_max.append(self.request.POST.getall('duAgemaxNew'+str(i)))
                du_qual_min.append(self.request.POST.getall('duQualNewmin'+str(i)))
                du_qual_max.append(self.request.POST.getall('duQualNewmax'+str(i)))
            for i in range(d_count):    # Run through days
                distance = Distance(competition=competition, day_numb=i, type=disciplines[i], lent=lengths[i])
                distance.save()
                dizs.append(zip(diz_groups[i], diz_length[i], diz_class[i], diz_min_com[i], diz_max_com[i]))
                dus.append(zip(du_group[i], du_salary[i], du_age_min[i], du_age_max[i], du_qual_min[i], du_qual_max[i]))
                for j in range(len(du_group[i])):      # Run through groups in one day
                    mem = MemInfo(salary=float(du_salary[i][j]), age_min=int(du_age_min[i][j]),
                                  age_max=int(du_age_max[i][j]), qual_min=du_qual_min[i][j], qual_max=du_qual_max[i][j])
                    mem.save()
                    dist = DistInfo(group_name=diz_groups[i][j], length=float(diz_length[i][j]),
                                    dist_class=int(diz_class[i][j]), min_com=int(diz_min_com[i][j]),
                                    max_com=int(diz_max_com[i][j]), mem_info=mem, distance=distance)
                    dist.save()

            temp_values = {'user_email': email, 'logout': users.create_logout_url('/login'), 'start': start_date,
                           'finish': finish_date, 'name': comp_name, 'show_places': show_places, 'show_map': show_map,
                           'days_count': range(1, int(d_count) + 1), 'pz_end_add': pz_end_add, 'pz_end_change':
                               pz_end_change, 'links': links, 'places': places, 'pzs': pzs, 'tzs': tzs, 'org_infos': orgs,
                           'discs': disciplines, 'lens': lengths, 'dizs':dizs, 'dus':dus, 'stat_day':stat_day, 'stat_sex':stat_sex,
                           'stat_qual':stat_qual}

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
    def get(self):  # shows info about competition that is stored in databasee
        user = users.get_current_user()
        if not user:
            email = 'Anonymous'
            role = 'Anonim'
        else:
            email = user.email()
            role = user.nickname()
            key = self.request.GET['dbKey']
            comp = Competition.get(key)
            infos = comp.info_set.run(batch_size=1000)
        temp_values = {'user_email': email, 'logout': users.create_logout_url('/login'), 'start': formatDate(str(comp.d_start)),
                       'finish': formatDate(str(comp.d_finish)), 'name': comp.name,
                       }

        #temp_values = {'user_email': email, 'logout': users.create_logout_url('/login'), 'start': start_date,
        #               'finish': finish_date, 'name': comp_name, 'show_places': show_places, 'show_map': show_map,
        #               'days_count': range(1, int(d_count) + 1), 'pz_end_add': pz_end_add, 'pz_end_change':
        #                   pz_end_change, 'links': links, 'places': places, 'pzs': pzs, 'tzs': tzs, 'org_infos': orgs,
        #               'discs': disciplines, 'lens': lengths, 'dizs': dizs, 'dus': dus, 'stat_day': stat_day,
        #               'stat_sex': stat_sex,
        #               'stat_qual': stat_qual}



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

def dateToPython(string_date):
    if '.' in string_date:
        dmy = string_date.split('.')
        d = int(dmy[0])
        m = int(dmy[1])
        y = int(dmy[2])
        return date(y, m, d)
    else:
        ymd = string_date.split('-')
        y = ymd[0]
        m = ymd[1]
        d = ymd[2]
        return date(y, m, d)

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

def onToBoolean(on_off):
    if str(on_off).find('on') > 0:
        return True
    else:
        return False

def readCheckboxPost(request, post_name):
    try:
        bool_value = request.request.POST[post_name]
        bool_value = True
    except:
        bool_value = False
    return bool_value

def readCheckboxGet(request, get_name):
    try:
        bool_value = request.request.GET[get_name]
        bool_value = True
    except:
        bool_value = False
    return bool_value
