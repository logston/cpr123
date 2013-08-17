from django.conf.urls import patterns, include, url

from apps.ewatch import views

urlpatterns = patterns('',
        url(r'^$', views.index),
        )
