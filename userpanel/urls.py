from django.conf.urls import patterns, include, url
from userpanel.views import userPanel
from userpanel.controllers import changeDays, changeName, changeFoodOrder, changeBanFood, changeStu

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',userPanel),
    url(r'^change_days/',changeDays),
    url(r'^change_name/',changeName),
    url(r'^change_food_order/',changeFoodOrder),
    url(r'^change_ban_food/',changeBanFood),
    url(r'^change_stu/',changeStu),
)
