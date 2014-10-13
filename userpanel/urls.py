from django.conf.urls import patterns, include, url
from userpanel.views import userPanel
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',userPanel),
)
