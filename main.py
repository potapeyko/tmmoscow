#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from ListHandlers import *
from CompetitionHandlers import *
from OtherHandlers import *
from modelVisitor import *

import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

import webapp2

class Test(webapp2.RequestHandler):
    def get(self):
        cur_user = users.get_current_user()
        cur_lead = db.Query(Leader).filter('user =', cur_user).get()
        user_members = db.Query(Member).filter('leader =', cur_lead)
        usrs = cur_user.nickname() + '  ALL::: '
        for m in user_members:
            usrs = usrs + m.nickname + ' - ' + m.leader.nickname + ' | '
        temp_values = {'test_data': usrs}
        self.response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/tmp.html').render(temp_values))


app = webapp2.WSGIApplication([
    ('/', DefaultHandler),
    ('/login', LoginHandler),
    ('/competition', CertainCompetition),
    ('/reg/newCompetition', NewCompetitionInfo),
    ('/reg/addCompetition', NewCompetition),
    ('/reg/memberList', MembersHandler),
    ('/reg/leaderList', LeadersHandler),
    ('/reg/organizerList', OrganizersHandler),
    ('/reg/addLeader', AddLeader),
    ('/reg/deleteLeader', DeleteLeader),
    ('/reg/addMember', AddMember),
    ('/reg/deleteMember', DeleteMember),
    ('/reg/addOrganizer', AddOrganizer),
    ('/reg/deleteOrganizer', DeleteOrganizer),
    ('/reg/searchOrganizer', OrganizersHandler),
    ('/test', Test),

], debug=True)

def handle_401(request, response, exception):
    response.set_status(401)
    temp_values = {'img_src':'../../static/img/er401.png', 'er_name':'401', 'back_redir':request.referer}
    response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))
def handle_403(request, response, exception):
    response.set_status(403)
    temp_values = {'img_src':'../../static/img/er403.png', 'er_name':'403', 'back_redir':request.referer}
    response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))
def handle_404(request, response, exception):
    response.set_status(404)
    temp_values = {'img_src':'../../static/img/er404.png', 'er_name':'404', 'back_redir':request.referer}
    response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))
def handle_405(request, response, exception):
    response.set_status(405)
    temp_values = {'img_src':'../../static/img/er405.png', 'er_name':'405'}
    response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))
def handle_500(request, response, exception):
    response.set_status(500)
    temp_values = {'img_src':'../../static/img/er500.png', 'er_name':'500', 'back_redir':request.referer}
    response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))
def handle_503(request, response, exception):
    response.set_status(503)
    temp_values = {'img_src':'../../static/img/er503.png', 'er_name':'503', 'back_redir':request.referer}
    response.write(JINJA_ENVIRONMENT.get_template('templates/tmmosc/ErrorPage.html').render(temp_values))

app.error_handlers[401] = handle_401
app.error_handlers[403] = handle_403
app.error_handlers[404] = handle_404
app.error_handlers[405] = handle_405
app.error_handlers[500] = handle_500
app.error_handlers[503] = handle_503
