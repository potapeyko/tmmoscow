__author__ = 'Daria'

from google.appengine.api import users
import os
import jinja2
import webapp2
from modelCompetition import Competition, Info
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
            d_start = []; d_finish = []; pzs = []
            for c in comps:
                d_start.append(str(c.d_start))
                d_finish.append(str(c.d_finish))
            d_start = formatDateList(d_start)
            d_finish = formatDateList(d_finish)
        temp_values = {'user_email': email, 'user_role': role, 'logout': users.create_logout_url('/login'), 'comps': comps,
                       'd_start': d_start, 'd_finish': d_finish}
        template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/organizer/CompetitionList.html')
        self.response.write(template.render(temp_values))
