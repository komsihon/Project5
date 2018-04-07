from django.conf.urls import patterns, include, url
from django.contrib import admin
from ikwen.flatpages.views import FlatPageView

from support.views import SupportList, Search, SupportDetails, AdminHome, save_pertinence, TopicList, get_media, delete_photo

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', SupportList.as_view(), name='home'),
    url(r'^ikwen/', include('ikwen.core.urls', namespace='ikwen')),
    url(r'^search/$', Search.as_view(), name='search'),
    url(r'^yommax/$', AdminHome.as_view(), name='admin_home'),
    url(r'^laakam/', include(admin.site.urls)),
    url(r'^give_point_of_view$', save_pertinence, name='give_point_of_view'),
    url(r'^(?P<application_slug>[-\w]+)/$', TopicList.as_view(), name='topic_list'),
    url(r'^(?P<application_slug>[-\w]+)/(?P<sub_chapter_slug>[-\w]+)$', SupportDetails.as_view(), name='support_detail'),
    url(r'^page/(?P<url>[-\w]+)/$', FlatPageView.as_view(), name='flatpage'),
    url(r'^get_media$', get_media, name='get_media'),
    url(r'^delete_photo$', delete_photo, name='delete_photo'),

)
