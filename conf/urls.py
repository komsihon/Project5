from django.conf.urls import patterns, include, url
from django.contrib import admin
from ikwen.flatpages.views import FlatPageView

from support.views import Home, Search, TopicDetail, AdminHome, submit_review, TopicList, get_media, delete_photo

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^ikwen/', include('ikwen.core.urls', namespace='ikwen')),
    url(r'^search/$', Search.as_view(), name='search'),
    url(r'^yommax/$', AdminHome.as_view(), name='admin_home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^submit_review$', submit_review, name='submit_review'),
    url(r'^(?P<application_slug>[-\w]+)/$', TopicList.as_view(), name='topic_list'),
    url(r'^(?P<application_slug>[-\w]+)/(?P<topic_slug>[-\w]+)$', TopicDetail.as_view(), name='topic_detail'),
    url(r'^page/(?P<url>[-\w]+)/$', FlatPageView.as_view(), name='flatpage'),
    url(r'^get_media$', get_media, name='get_media'),
    url(r'^delete_photo$', delete_photo, name='delete_photo'),
)
