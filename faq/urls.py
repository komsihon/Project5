from django.conf.urls import include, patterns, url
from django.conf import settings
# from django.urls import path
from django.contrib import admin
from faq.views import HomeView, TopicView, GeneralView, QuestionList, user_feedback, autocomplete_infos
urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='faqhome'),
    url(r'^general$', GeneralView.as_view(), name='general'),
    url(r'^(?P<app_slug>[-\w]+)/(?P<category_slug>[-\w]+)/(?P<question_slug>[-\w]+)$',
        TopicView.as_view(), name='topic'),
    url(r'^question_list/$', QuestionList.as_view(), name='question_list'),
    url(r'^user_feedback/$', user_feedback, name='user_feedback'),
    url(r'^autocomplete_infos/$', autocomplete_infos, name='autocomplete_infos'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)
