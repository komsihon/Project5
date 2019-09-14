from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from ikwen.flatpages.views import FlatPageView
from ikwen.core.views import upload_image, upload_customization_image

from support.views import Home, Search, TopicDetail, AdminHome, submit_review, TopicList, get_media, delete_photo

admin.autodiscover()
urlpatterns = patterns(
    '',
    # url(r'^$', Home.as_view(), name='home'),
    url(_(r'^'), include('faq.urls')),
    url(r'^ikwen/', include('ikwen.core.urls', namespace='ikwen')),
    url(r'^search/$', Search.as_view(), name='search'),
    url(r'^yommax/$', AdminHome.as_view(), name='admin_home'),
    url(r'^laakam/', include(admin.site.urls)),
    url(r'^submit_review$', submit_review, name='submit_review'),
    url(r'^(?P<application_slug>[-\w]+)/$', TopicList.as_view(), name='topic_list'),
    url(r'^(?P<application_slug>[-\w]+)/(?P<topic_slug>[-\w]+)$', TopicDetail.as_view(), name='topic_detail'),
    url(r'^page/(?P<url>[-\w]+)/$', FlatPageView.as_view(), name='flatpage'),
    url(r'^get_media$', get_media, name='get_media'),
    url(r'^delete_photo$', delete_photo, name='delete_photo'),
    url(r'^upload_image$', upload_image, name='upload_image'),
)
