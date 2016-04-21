__author__ = 'Daria'

from google.appengine.api import users
from datetime import datetime
import os
import jinja2
import webapp2
from google.appengine.ext import db
from modelCompetition import Competition, Info, MemInfo, DistInfo, Distance
from CompetitionHandlers import formatDateList

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# LogIn / Registration page
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email = user.email()
            temp_values = {'user_email':email}
            template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/organizer/CompetitionList.html')
            self.response.write(template.render(temp_values))
        else:
            self.redirect(users.create_login_url('/'))
      #  temp_values = {}
      #  template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/LogIn.html')
      #  self.response.write(template.render(temp_values))
    def post(self):
        self.response.write('POST Registration of user')



# Competition list
class DefaultHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            email = 'Anonymous'
            role = 'Anonim'
        else:
            email = user.email()
            role = user.nickname()
            comps = Competition.all().order('d_start')
            d_start = []; d_finish = []; pzs = []; pzs_add_end = []; is_open = []
            for c in comps:
                d_start.append(str(c.d_start))
                d_finish.append(str(c.d_finish))
                infos_of_comp = c.info_set.get()        # Returns one or several Info objects (instance or list)
                is_open.append(infos_of_comp.pz_is_open)





            d_start = formatDateList(d_start)
            d_finish = formatDateList(d_finish)
        temp_values = {'user_email': email, 'user_role': role, 'logout': users.create_logout_url('/login'), 'comps': comps,
                       'd_start': d_start, 'd_finish': d_finish, 'pzs': pzs, 'test': infos_of_comp, 'is_open': is_open}
        template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/organizer/CompetitionList.html')
        self.response.write(template.render(temp_values))
