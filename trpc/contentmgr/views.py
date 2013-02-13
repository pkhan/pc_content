from contentmgr.models import Content, CatIntro, Entry
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.utils import timezone

def home(request, category):
    intro = None
    intros = CatIntro.objects.filter(draft=False).filter(main_cat=category).order_by('-pub_date')[0:1]
    if len(intros) > 0:
        intro = intros[0]
    entries = Entry.objects.all().order_by('-pub_date').filter(pub_date__lte=timezone.now()).filter(draft=False)
    if category != '':
        entries = entries.filter(main_cat=category)
    c = RequestContext(request, { 'entries' : entries,
        'intro' : intro } )
    t = loader.get_template('index.html')
    output = t.render(c)
    return HttpResponse(output)

def detail(request, category, content_id):
    return HttpResponse("HI")

def edit(request, category, content_id):
    return HttpResponse("EDIT")
