from django.conf.urls import patterns, url
from api.controllers import user_credit, this_week_foods, set_cookie, get_cookie, del_cookie

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'reserver.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^userCredit/', user_credit),
                       url(r'^thisWeek/', this_week_foods),
                       url(r'^sendcookie/', set_cookie),
                       url(r'^getcookie/', get_cookie),
                       url(r'^delcookie/', del_cookie),
)
