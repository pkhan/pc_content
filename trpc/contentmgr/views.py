from contentmgr.models import Content, CatIntro, Entry, User
from contentmgr.forms import ContentForm
from django.template import loader, Context, RequestContext
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as r_login
from django.contrib.auth.decorators import login_required

def home(request, category):
    show_edit = request.user.is_authenticated()
    intro = None
    intros = CatIntro.objects.filter(draft=False).filter(main_cat=category).order_by('-pub_date')[0:1]
    if len(intros) > 0:
        intro = intros[0]
    entries = Entry.objects.all().order_by('-pub_date').filter(pub_date__lte=timezone.now()).filter(draft=False)
    tags = []
    if category != 'home':
        entries = entries.filter(main_cat=category)
    highlights = entries.order_by('-highlight')[0:5]
    c = RequestContext(request, { 'entries' : entries[0:10],
        'highlights' : highlights,
        'tags' : tags,
        'intro' : intro,
        'category' : category,
        'show_edit' : show_edit } )
    t = loader.get_template('index.html')
    output = t.render(c)
    return HttpResponse(output)

def detail(request, content_id, category):
    try:
        e = Content.objects.filter(main_cat=category).get(pk=content_id)
    except Entry.DoesNotExist:
        raise Http404

    t = loader.get_template('view.html')
    c = RequestContext(request, { 'content' : e, 'category' : category })

    return HttpResponse(t.render(c))

@login_required
def edit(request, category, content_id):
    t = loader.get_template('edit.html')
    try:
        content = Content.objects.get(pk = content_id)
    except Content.DoesNotExist:
        raise Http404
    form = ContentForm(instance = content)

    c = RequestContext(request,{ 'form' : form, 'content' : content } )
    return HttpResponse(t.render(c))

@login_required
def create(request, category, intro=False):
    if intro:
        try:
            e = CatIntro.objects.filter(main_cat=category)[0:1].get()
        except CatIntro.DoesNotExist:
            e = CatIntro()
    else:
        e = Entry()

    e.author = request.user
    e.main_cat = category
    e.save()
    
    return redirect('edit', category=category, content_id=e.id)

@login_required
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

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        r_login(request, user)
        redir = None
        if 'next' in request.GET.keys():
            redir = request.GET['next']
        if redir:
            return redirect(redir)
        return redirect('home', category='home')
    return HttpResponse( loader.get_template('login.html').render(RequestContext(request, {})) )

