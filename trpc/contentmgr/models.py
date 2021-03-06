from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as n_User
from markdown import markdown

class Content(models.Model):
    title = models.CharField(max_length=200, default="")
    author = models.ForeignKey(n_User, null=True, blank=True, default=1)
    pub_date = models.DateTimeField(null=True, blank=True)
    mod_date = models.DateTimeField(auto_now=True)
    draft = models.BooleanField(default=True)
    main_cat = models.CharField(max_length=50, default="", blank=True)
    body = models.TextField(default="")
    tags = models.ManyToManyField('Tag', blank=True)
    highlight = models.IntegerField(default=0)

    def publish(self):
        self.draft = False
        if self.pub_date is None:
            self.pub_date = timezone.now()

    def get_html(self):
        return markdown(self.body)

    def get_short_html(self):
        tail = ''
        if len(self.body) > 300:
            tail = '...'
        return markdown(self.body[0:300]+tail)
    
    def __unicode__(self):
        return self.title

class Entry(Content):
    pass

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    trusted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    tag = models.CharField(max_length=50, primary_key=True)

    def __unicode__(self):
        return self.tag

class CatIntro(Content):
    pass
