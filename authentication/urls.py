from django.conf.urls import patterns, include, url
from authentication.controllers import *
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^signin/',signIn),
    url(r'^login/',login),
    url(r'^logout/',logout),
    url(r'^debug_active/',debugActiveUser),
)
