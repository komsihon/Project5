from django.conf.urls import patterns, url
from django.contrib import admin
from support.views import Home, TopicDetail, Search

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', Home.as_view(), name='community_list'),
                       url(r'^(?P<slug>[-\w]+)/tuto$', TopicDetail.as_view(), name='community_detail'),
                       )
