import os
import logging
import wsgiref.handlers
import webapp2
from webapp2_extras import sessions
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Employee(db.Model):
  name = db.StringProperty(required=True)
  role = db.StringProperty(required=True,
                           choices=set(["executive", "manager", "producer"]))

e1 = Employee(name="John",
             role="manager")
e1.put()


e2 = Employee(name="Jack",
             role="producer")
e2.put()



def doRender(handler, tname, values={}):
	temp = os.path.join(
	os.path.dirname(__file__), 
	'templates/' + tname)
	if not os.path.isfile(temp):
		return False
	# Make a copy and add the path
	newval = dict(values)
	newval['path'] = handler.request.path
	outstr = template.render(temp, newval)
	handler.response.out.write(outstr)
	return True

	
class MainHandler(webapp2.RequestHandler):
	def get(self):
		que = db.Query(Employee)
		user_list = que.fetch(limit=2)
		doRender(self, 'memberscreen.html', 
		{'user_list': user_list})


application = webapp2.WSGIApplication([
	('/', MainHandler)],
	debug=True)
wsgiref.handlers.CGIHandler().run(application)	
 
 
 


