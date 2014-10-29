from django.conf.urls import patterns, url
from api.controllers import user_credit, this_week_foods

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'reserver.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^userCredit/', user_credit),
                       url(r'^thisWeek/', this_week_foods),
)
