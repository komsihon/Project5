from django.conf.urls import include, patterns, url
from django.conf import settings
# from django.urls import path
from django.contrib import admin
from faq.views import Home, TopicDetails, ApplicationCategoriesList, QuestionList, save_user_feedback, autocomplete_user_research
urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='faqhome'),
    url(r'^(?P<app_slug>[-\w]+)$', ApplicationCategoriesList.as_view(), name='app_categories_list'),
    url(r'^(?P<app_slug>[-\w]+)/(?P<category_slug>[-\w]+)/(?P<question_slug>[-\w]+)$',
        TopicDetails.as_view(), name='topic_detail'),
    url(r'^question_list/$', QuestionList.as_view(), name='question_list'),
    url(r'^save_user_feedback/$', save_user_feedback, name='save_user_feedback'),
    url(r'^autocomplete_user_research/$', autocomplete_user_research, name='autocomplete_user_research'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)
