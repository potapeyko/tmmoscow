from google.appengine.api import users
from datetime import datetime
import os
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class memberInfo(webapp2.RequestHandler):
    def get(self):
        login = users.create_login_url(dest_url='/postSignIn')
        temp_values = {'login': login, 'logout': users.create_logout_url('/login')}
        template = JINJA_ENVIRONMENT.get_template('/templates/tmmosc/member/MemberView.html')
        self.response.write(template.render(temp_values))

    def post(self):
        self.response.write('POST from memberInfo')

