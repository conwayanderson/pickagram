from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'project.core.views.home', name='home'),
    url(r'^pick/$', 'project.core.views.pick', name='pick'),
    url(r'^like/(?P<media_id>[0-9_]+)/$', 'project.core.views.like', name='like'),
    url(r'^oauth_callback/$', 'project.core.views.oauth_callback', name='oauth-callback'),
    url(r'^oauth_logout/$', 'project.core.views.oauth_logout', name='oauth-logout'),
)
