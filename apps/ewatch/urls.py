from django.conf.urls import patterns, include, url

from apps.ewatch import views

urlpatterns = patterns('',
        url(r'^$', views.index),
        url(r'^scrape_details/$', views.scrape_details),
        url(r'^tally_classes/$', views.tally_classes2),
		#url(r'^tally_regs/$', views.tally_regs),
		url(r'^tally_revenue/$', views.tally_revenue),
        )