from django.forms import ModelForm
from contentmgr.models import Content

class ContentForm(ModelForm):
    class Meta:
        model = Content
        exclude = ('author', 'pub_date')
