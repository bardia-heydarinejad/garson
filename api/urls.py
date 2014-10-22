from django.conf.urls import patterns, url
from api.controllers import user_credit, today_lunch

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'reserver.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^userCredit/', user_credit),
                       url(r'^todayLunch/', today_lunch),
)
