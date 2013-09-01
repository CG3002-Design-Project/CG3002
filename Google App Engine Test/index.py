import os
import logging
import wsgiref.handlers
import webapp2
from webapp2_extras import sessions
from google.appengine.ext import db
from google.appengine.ext.webapp import template


class User(db.Model):
 account = db.StringProperty()
 password = db.StringProperty()
 name = db.StringProperty()
 
def doRender(handler, tname, values={}):
	 temp = os.path.join(
	 os.path.dirname(__file__), 
	 'templates/' + tname)
	 if not os.path.isfile(temp):
		return False
	 # Make a copy and add the path
	 outstr = template.render(temp, {})
	 handler.response.out.write(outstr)
	 return True
 
class MainHandler(webapp2.RequestHandler):

	def get(self):
	    doRender(self, 'loginscreen.html',{})

 
class ApplyHandler(webapp2.RequestHandler):

	def get(self):
		doRender(self, 'applyscreen.html',{})

	def post(self):
		self.session = Session()
		name = self.request.get('name')
		acct = self.request.get('account')
		pw = self.request.get('password')
		logging.info('Adding account='+acct)
	
		newuser = User(name=name, account=acct, password=pw);
		newuser.put();



application = webapp2.WSGIApplication([
	('/apply', ApplyHandler),
	('/', MainHandler)],
	debug=True)
wsgiref.handlers.CGIHandler().run(application)	