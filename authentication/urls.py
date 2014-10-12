from django.conf.urls import patterns, include, url
from authentication.views import signIn
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^signin/',signIn),
)
