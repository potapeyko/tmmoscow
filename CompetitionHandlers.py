__author__ = 'Daria'

from google.appengine.api import users
import os
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class NewCompetition(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email = user.email()
            temp_values = {'user_email':email, 'logout':users.create_logout_url('/login')}
            template = JINJA_ENVIRONMENT.get_template('templates/tmmosc/organizer/AddCompetition.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = {'img_src':'../static/img/er401.png', 'er_name':'401', 'login_redir':users.create_login_url('/reg/newCompetition')}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))
    def post(self):
        self.response.write('POST Save new info about competition (ORG)')

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
