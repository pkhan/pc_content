from contentmgr.models import Content, CatIntro, Entry, User
from contentmgr.forms import ContentForm
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
    if category != 'home':
        entries = entries.filter(main_cat=category)
    c = RequestContext(request, { 'entries' : entries,
        'intro' : intro } )
    t = loader.get_template('index.html')
    output = t.render(c)
    return HttpResponse(output)

def detail(request, content_id, category):
    try:
        e = Content.objects.filter(main_cat=category).get(pk=content_id)
    except Entry.DoesNotExist:
        raise Http404
    return HttpResponse(e.get_html())

def edit(request, category, content_id):
    t = loader.get_template('edit.html')
    try:
        content = Content.objects.get(pk = content_id)
    except Content.DoesNotExist:
        raise Http404
    form = ContentForm(instance = content)

    c = RequestContext(request,{ 'form' : form, 'content' : content } )
    return HttpResponse(t.render(c))

def create(request, category, intro=False):
    if intro:
        try:
            e = CatIntro.objects.filter(main_cat=category)[0:1].get()
        except CatIntro.DoesNotExist:
            e = CatIntro()
    else:
        e = Entry()

    e.author = User.objects.all()[0]
    e.main_cat = category
    e.save()
    
    return redirect('edit', category=category, content_id=e.id)

def update(request, content_id):
    content = Content.objects.get(pk=content_id)
    if request.method == 'POST':
        form = ContentForm(request.POST, instance=content)
    else:
        raise Http404

    content = form.save(commit=False)

    if 'button' in request.POST:
        if request.POST['button'] == 'Publish':
            content.publish()
        content.save()
        return redirect('detail', category=content.main_cat, content_id=content.id)

    return HttpResponse('OK')
