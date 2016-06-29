# -*- coding: utf-8 -*-
import os
import jinja2
from google.appengine.api import users

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
