from contentmgr.models import Content
from django.template import loader, Context, RequestContext
from django.http import HttpResponse

def home(request):
    contents = Content.objects.all().order_by('-pub_date')
    c = RequestContext(request, { 'content_list' : contents } )
    t = loader.get_template('index.html')
    output = t.render(c)
    return HttpResponse(output)

def detail(request, content_id):
    return HttpResponse("HI")

def edit(request, content_id):
    return HttpResponse("EDIT")
