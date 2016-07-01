# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
from google.appengine.api import users
from webapp2_extras import sessions

__author__ = 'Daria'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# check is user authorized to look at some secured part of the system
def show_unauth_page(self):
    temp_values = {'img_src': '../static/img/er401.png', 'er_name': '401', 'login_redir':
                    users.create_login_url('/postSignIn')}
    self.response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))


class BaseHandler(webapp2.RequestHandler):

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()