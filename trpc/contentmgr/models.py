from django.db import models
from django.utils import timezone
from markdown import markdown

class Content(models.Model):
    title = models.CharField(max_length=200,default="")
    author = models.ForeignKey('User')
    pub_date = models.DateField(null=True, blank=True)
    mod_date = models.DateField(auto_now=True)
    draft = models.BooleanField(default=True)
    body = models.TextField(default="")

    def publish(self):
        self.draft = False
        if self.pub_date is None:
            self.pub_date = timezone.now()

    def get_html(self):
        return markdown(self.body)
    
    def __unicode__(self):
        return self.title

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    trusted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
