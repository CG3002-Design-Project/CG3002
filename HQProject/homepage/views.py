#from django.http import HttpResponse, HttpResponseRedirect
#from django.contrib import auth
#from django.template import Context, RequestContext, loader
#from django.shortcuts import render_to_response 
#from django.core.context_processors import csrf
#from django.contrib.auth import authenticate, login
#from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template import Context, loader, RequestContext

from django.shortcuts import render_to_response
#
@login_required
def garbage_stat_info(request):
    template = loader.get_template('stat_info.html')
    context = Context({'is_auth': str(request.user.is_authenticated())})
    return HttpResponse(template.render(context))

@login_required
def stat_info(request):
    return render_to_response('stat_info.html',
        {'is_auth':request.user.is_authenticated()},
        context_instance=RequestContext(request))

@login_required
def mainmenu(request):
    return render_to_response('mainmenu.html',{},
        context_instance=RequestContext(request))
#def login(request):
 #   c = {}
  #  c.update(csrf(request))
  #  return render_to_request('login.html', c)

#def index(request):
 #   template = loader.get_template('homepage/home.html')
    #context = RequestContext(request, {
     #   'latest_poll_list': latest_poll_list,
   # })
  #  return HttpResponse(template.render(request))
    #return render(request, 'homepage/home.html') 
