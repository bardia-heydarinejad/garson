from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'reserver.views.home', name='home'),

    url(r'^authentication/', include("authentication.urls")),
    url(r'^account/', include("userpanel.urls")),
    url(r'^api/', include("api.urls")),
    url(r'^kerm_haye_koon/', include(admin.site.urls)),
)+staticfiles_urlpatterns()
