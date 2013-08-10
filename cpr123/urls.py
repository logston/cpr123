from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

subdir = r'^cpr123/'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cpr123.views.home', name='home'),
    # url(r'^cpr123/', include('cpr123.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(subdir+r'admin/', include(admin.site.urls)),
    
    url(subdir+r'ewatch/', include('ewatch.urls')),

)
