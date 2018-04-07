from django.conf.urls import patterns, url
from django.contrib import admin
from support.views import SupportList, SupportDetails, Search

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', SupportList.as_view(), name='community_list'),
                       url(r'^(?P<slug>[-\w]+)/tuto$', SupportDetails.as_view(), name='community_detail'),
                       )
