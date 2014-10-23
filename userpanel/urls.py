from django.conf.urls import patterns, url
from userpanel.views import user_panel
from userpanel.controllers import change_days, change_food_order, change_email

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'reserver.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', user_panel),
                       url(r'^change_days/', change_days),
                       url(r'^change_email/', change_email),
                       url(r'^change_food_order/', change_food_order),
)
