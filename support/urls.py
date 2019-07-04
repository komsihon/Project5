from django.conf.urls import patterns, url
from django.contrib import admin

from support.views import Home, TopicDetail, Search, TopicList, submit_review

admin.autodiscover()

urlpatterns = patterns('',
                       # url(r'^$', Home.as_view(), name='home'),
                       # url(r'^give_point_of_view$', save_pertinence, name='give_point_of_view'),
                       # url(r'^(?P<application_slug>[-\w]+)/$', TopicList.as_view(), name='topic_list'),
                       # url(r'^(?P<application_slug>[-\w]+)/(?P<sub_chapter_slug>[-\w]+)$', TopicDetail.as_view(), name='support_detail'),
                       )