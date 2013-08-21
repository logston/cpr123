from django.conf.urls import patterns, include, url

from apps.ewatch import views

urlpatterns = patterns('',
        url(r'^$', views.index),
        url(r'^list_classes/$', views.list_classes),
        url(r'^scrape_details/$', views.scrape_details),
        )
