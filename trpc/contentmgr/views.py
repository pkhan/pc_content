from contentmgr.models import Content
from django.http import HttpResponse

def home(request):
    contents = Content.objects.all().order_by('-pub_date')
    output = '<p></p>'.join([c.get_html() for c in contents])
    return HttpResponse(output)
