from django.conf.urls import patterns, include, url

from apps.ewatch import views

urlpatterns = patterns('',
        url(r'^$', views.index),
        url(r'^scrape_details/$', views.scrape_details),
        url(r'^tally_classes/$', views.tally_classes2),
		#url(r'^tally_regs/$', views.tally_regs),
		url(r'^tally_revenue/$', views.tally_revenue),
		url(r'^enrollment_by_zip/$', views.heatmap),
        )

urlpatterns += patterns('',
	url(r'^distribution/registration_times/$', views.dist_of_reg_times),
	)

urlpatterns += patterns('',
	url(r'^figure/registration_times/$', views.dist_of_reg_times_fig),
	)

print (urlpatterns)