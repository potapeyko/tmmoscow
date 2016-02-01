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

class NewCompetition(webapp2.RequestHandler):
    def get(self):  # shows empty form for adding new competition
        user = users.get_current_user()
        if user:
            email = user.email()
            temp_values = {'user_email':email, 'logout':users.create_logout_url('/login')}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/AddCompetition.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = {'img_src':'../static/img/er401.png', 'er_name':'401', 'login_redir':users.create_login_url('/reg/newCompetition')}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))
    def post(self): # save filled form about new competition
        user = users.get_current_user()
        if user:
            email = user.email()
            # common info about competition
            logo = self.request.POST['logoNew']
            start_date = self.request.POST['dateStartNew']
            finish_date = self.request.POST['dateFinishNew']
            comp_name = self.request.POST['nameCompNew']
            count_start = self.request.POST['countStart']
            start_places = self.request.POST['startPlaces']
            # info about each day
            pz = self.request.POST.getall('trPzNew')                        # list of triggers is PZ open
            pz_end_add = self.request.POST.getall('pzEndAddNew')            # list of dates when PZ will be closed to adding
            pz_end_change = self.request.POST.getall('pzEndChangeNew')      # list of dates when PZ will be closed to changing
            tz = self.request.POST.getall('trTzNew')                        # list of triggers is TZ open
            link_to_tmmosc = self.request.POST.getall('toTmMoscowNew')      # list of link to official site
            org_fios = self.request.POST.getall('orgFioNew')                # list of organizer's fios
            org_dols = self.request.POST.getall('orgDolNew')                # list of organizer's dols
            org_contacts = self.request.POST.getall('orgContNew')           # list of organizer's contacts
            org_info = []
            for i in range(0, len(org_fios)):
                org_info.append([org_fios[i], org_dols[i], org_contacts[i]])
            # info about distances
            disciplines = self.request.POST['dizDisciplineNew']             # list of all disciplines for all days
            lengths = self.request.POST['dizLengthNew']                     # list of all lengths for all days
            groups_info = []
            for day_num in range(0, count_start):
                groups_for_day = self.request.POST['dizGroupNew'+str(day_num)]
                lengths_for_day = self.request.POST['dizLenNew'+str(day_num)]
                classes_for_day = self.request.POST['dizClassNew'+str(day_num)]
                min_comm_for_day = self.request.POST['dizCCminNew'+str(day_num)]
                max_comm_for_day = self.request.POST['dizCCmaxNew'+str(day_num)]
                groups_info.append([groups_for_day, lengths_for_day, classes_for_day, min_comm_for_day, max_comm_for_day])
            members_info = []
            for day_num in range(0, count_start):
                groups_info[i][0]
                salary_for_day = self.request.POST['duSalaryNew'+str(day_num)]
                min_age = self.request.POST['duAgeminNew'+str(day_num)]
                max_age = self.request.POST['duAgemaxNew'+str(day_num)]
                min_qual = self.request.POST['duQualNewmin'+str(day_num)]
                max_qual = self.request.POST['duQualNewmax']+str(day_num)


            temp_values = {'user_email':email, 'logout':users.create_logout_url('/login'),   'logo':logo, 'start':start_date,
                           'finish': finish_date, 'name':comp_name, 'count_start':count_start, 'start_places':start_places,
                           'pzs':pz, 'pzEndAdds':pz_end_add, 'pzEndChanges':pz_end_change, 'tzs':tz, 'links':link_to_tmmosc,
                           'orgs': org_info}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/Competition.html')
            #template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/AddCompetition.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = {'img_src':'../static/img/er401.png', 'er_name':'401', 'login_redir':users.create_login_url('/reg/newCompetition')}
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
        temp_values = {'user_email':email, 'logout':users.create_logout_url('/login')}
        template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/Competition.html')
        self.response.write(template.render(temp_values))
    def post(self):
        self.response.write('POST Add new info about competition (ORG)')
