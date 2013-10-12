# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.
def index(request):
    template = loader.get_template('userprofile/userprofile.html')
    #context = RequestContext(request, {
     #   'latest_poll_list': latest_poll_list,
   # })
    return HttpResponse(template.render(request))

