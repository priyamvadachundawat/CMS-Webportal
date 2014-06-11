from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'webportal.views.home', name='home'),
    url(r'^$', 'webapp.views.index'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^upload/$','webapp.views.contributor_upload'),

)
