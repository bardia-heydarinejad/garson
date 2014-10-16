from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'reserver.views.home', name='home'),

    url(r'^authentication/', include("authentication.urls")),
    url(r'^account/', include("userpanel.urls")),
    url(r'^admin/', include(admin.site.urls)),
)
