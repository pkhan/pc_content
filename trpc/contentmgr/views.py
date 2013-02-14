from contentmgr.models import Content, CatIntro, Entry, User
from django.template import loader, Context, RequestContext
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.shortcuts import redirect

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
    try:
        e = Entry.objects.filter(main_cat=category).get(pk=content_id)
    except Entry.DoesNotExist:
        raise Http404
    return HttpResponse(e.get_html())

def edit(request, category, content_id):
    return HttpResponse("EDIT")

def create(request, category, intro=False):
    print(category)
    print(intro)
    if intro:
        try:
            e = CatIntro.objects.filter(main_cat=category)[0:1].get()
            print("model is catintro")
        except CatIntro.DoesNotExist:
            e = CatIntro()
    else:
        e = Entry()

    e.author = User.objects.all()[0]
    e.main_cat = category
    #e.save()
    
    return HttpResponse("CREATE")
    return redirect('edit', category=category, content_id=e.id)

def update(request, content_id):
    pass
