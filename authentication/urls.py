from django.conf.urls import patterns, url
from authentication.controllers import login, logout

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'reserver.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^login/', login),
                       url(r'^logout/', logout),
)
