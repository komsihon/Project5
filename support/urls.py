from django.conf.urls import patterns, url
from django.contrib import admin
from support.views import SupportList, SupportDetails, Search, TopicList, save_pertinence

admin.autodiscover()

urlpatterns = patterns('',
                       # url(r'^$', SupportList.as_view(), name='home'),
                       # url(r'^give_point_of_view$', save_pertinence, name='give_point_of_view'),
                       # url(r'^(?P<application_slug>[-\w]+)/$', TopicList.as_view(), name='topic_list'),
                       # url(r'^(?P<application_slug>[-\w]+)/(?P<sub_chapter_slug>[-\w]+)$', SupportDetails.as_view(), name='support_detail'),
                       )