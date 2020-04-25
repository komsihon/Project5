from django.conf.urls import include, patterns, url
from django.conf import settings
# from django.urls import path
from django.contrib import admin
from django.contrib.auth.decorators import permission_required

from faq.views import Home, QuestionDetail, ShowTopicList, save_user_feedback, \
    autocomplete_user_research, TopicList, ShowQuestionList, QuestionList, \
    ChangeTopic, ChangeQuestion

urlpatterns = patterns(
    '',
    url(r'^yogam/topics/$', permission_required('faq.ik_manage_topics')(TopicList.as_view()), name='topic_list'),
    url(r'^yogam/changeTopic/$', permission_required('faq.ik_manage_topics')(ChangeTopic.as_view()),
        name='change_topic'),
    url(r'^yogam/changeTopic/(?P<object_id>[-\w]+)/$',
        permission_required('faq.ik_manage_topics')(ChangeTopic.as_view()), name='change_topic'),

    url(r'^yogam/questions/$', permission_required('faq.ik_manage_questions')(QuestionList.as_view()), name='question_list'),
    url(r'^yogam/changeQuestion/$', permission_required('faq.ik_manage_questions')(ChangeQuestion.as_view()),
        name='change_question'),
    url(r'^yogam/changeQuestion/(?P<object_id>[-\w]+)/$', permission_required('faq.ik_manage_questions')(ChangeQuestion.as_view()), name='change_question'),

    url(r'^questionList/$', ShowQuestionList.as_view(), name='show_question_list'),
    url(r'^save_user_feedback/$', save_user_feedback, name='save_user_feedback'),
    url(r'^autocomplete_user_research/$', autocomplete_user_research, name='autocomplete_user_research'),

    url(r'^(?P<app_slug>[-\w]+)$', ShowTopicList.as_view(), name='show_topic_list'),
    url(r'^(?P<app_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/(?P<question_slug>[-\w]+)$',
        QuestionDetail.as_view(), name='question_detail'),
)

