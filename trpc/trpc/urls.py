from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'contentmgr.views.home'),
    url(r'^view/(?P<content_id>\d+)/$', 'contentmgr.views.detail'),
    url(r'^edit/(?P<content_id>\d+)/$', 'contentmgr.views.edit')
    # Examples:
    # url(r'^$', 'trpc.views.home', name='home'),
    # url(r'^trpc/', include('trpc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
