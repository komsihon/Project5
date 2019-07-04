from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse
from django.http import Http404, HttpRequest, HttpResponse
from django.template import loader
from django.utils.translation import get_language
from django.views.i18n import set_language
from django.views.generic import TemplateView
from ikwen.core.utils import to_dict
from faq.models import *
from django.shortcuts import render
from forms import *

import json
import sys


reload(sys)
sys.setdefaultencoding('utf-8') # Allow system to decode utf-8's strings such as ',",|,?


def sentence_with_keyword(paragraph, keyword_word):
    sentence_list = []
    for sentence in paragraph.split('.'):
        if keyword_word in sentence:
            sentence_list.append(sentence+".\n")
    return sentence_list


class HomeView(TemplateView):
    template_name = 'faq/home_faq.html'

    def get_context_data(self, **kwargs):
        language = get_language()
        context = super(HomeView, self).get_context_data(**kwargs)
        app_list = []
        for app in Application.objects.all().order_by('name'):
            category_list = list(Category.objects.filter(app=app))
            topic_list = Topic.objects.filter(category__in=category_list, language__istartswith=language)
            if topic_list.count() > 0:
                app.topic_list = topic_list
                app_list.append(app)

        context['app_list'] = app_list
        return context


class TopicView(TemplateView):
    template_name = 'faq/topic.html'

    def get_context_data(self, **kwargs):
        context = super(TopicView, self).get_context_data()
        app_slug = kwargs['app_slug']
        category_slug = kwargs['category_slug']
        question_slug = kwargs['question_slug']
        question = Question.objects.get(slug=question_slug)
        category = Category.objects.get(slug=category_slug)
        app = Application.objects.get(slug=app_slug)
        current_language = get_language()
        prev_lang = question.language
        while category.language.lower() != current_language:
            category = category.translated_versions

        while question.language.lower() != current_language:
            print question.text
            question = question.translated_versions

        question = Question.objects.get(slug=question.slug, language__istartswith=current_language)
        topic = Topic.objects.filter(category=category, language__istartswith=current_language).get(question=question)
        context['app'] = app
        context['category'] = category
        context['question'] = question
        context['topic'] = topic
        # context['current_lang'] = current_language
        # context['prev_lang'] = prev_lang
        return context


class GeneralView(TemplateView):
    template_name = 'faq/general_faq.html'

    def get_context_data(self, **kwargs):
        language = get_language()
        context = super(GeneralView, self).get_context_data()
        category_list = []
        for category in Category.objects.filter(language__istartswith=language).order_by('name'):
            topic_list = []
            for topic in Topic.objects.filter(category=category, language__istartswith=language):
                topic_list.append(topic)
            category.topic_list = topic_list
            category_list.append(category)

        # question_list = []
        # for q in Question.objects.all():
        #     if q not in [topic.question for topic in Topic.objects.all()]:
        #         question_list.append(q)
        # question_list2 = []
        # for q in Question.objects.exclude(language__istartswith='en').exclude(language__istartswith='fr'):
        #     question_list2.append(q)
        context['category_list'] = category_list
        # context['question_list'] = question_list
        # context['question_list2'] = question_list2
        return context

    # def post


class QuestionList(TemplateView):
    template_name = 'faq/question_list.html'

    def get_context_data(self, **kwargs):
        language = get_language()
        context = super(QuestionList, self).get_context_data()
        q = self.request.GET["question"]
        topic_list = []
        category_list = list(Category.objects.filter(name__icontains=q, language__istartswith=language))
        question_list = list(Question.objects.filter(text__icontains=q, language__istartswith=language))

        for topic in Topic.objects.filter(language__istartswith=language).exclude(question__in=question_list):
            if q not in category_list:
                # topic.question not in question_list and
                topic.sentence_with_keyword = sentence_with_keyword(topic.answer, q)
                if topic.sentence_with_keyword.__len__() > 0:
                    topic_list.append(topic)

        for question in question_list:
            question.topic_set = []
            for topic in Topic.objects.filter(question=question, language__istartswith=language):
                question.topic_set.append(topic)

        context['question_list'] = question_list
        context['topic_list'] = topic_list
        context['category_list'] = category_list
        context['queried_question'] = q
        return context


def user_feedback(request, *args, **kwargs):
    language = get_language()
    q = request.GET
    topic = q.get('topic')
    matched_topic = Topic.objects.filter(language__istartswith=language).get(slug=topic)
    count_helpful = q.get('count_helpful')
    count_helpless = q.get('count_helpless')
    user_views = q.get('user_views')
    if user_views:
        matched_topic.user_views += int(user_views)
    if count_helpless or count_helpful:
        matched_topic.count_helpful += int(count_helpful)
        matched_topic.count_helpless += int(count_helpless)
    matched_topic.save()
    response = "Successfully receive the request"
    return HttpResponse(json.dumps({'success': True, 'count_helpful': matched_topic.count_helpful}), 'content-type: text/json')


def autocomplete_infos(request, *args, **kwargs):
    language = get_language()
    q = request.GET['q']
    topic_list_with_keyword_in_question = []
    topic_list_with_keyword_in_answer = []

    for topic in Topic.objects.filter(language__istartswith=language):
        topic.question_text = topic.question_text
        if q not in [category.name for category in Category.objects.filter(name__icontains=q)]:
            if topic.question in Question.objects.filter(text__icontains=q):
                topic_list_with_keyword_in_question.append(to_dict(topic))
            else:
                topic.sentence_with_keyword = sentence_with_keyword(topic.answer, q)
                if topic.sentence_with_keyword.__len__() > 0:
                    topic_list_with_keyword_in_answer.append(to_dict(topic))

    category_list = [to_dict(obj) for obj in Category.objects.filter(name__icontains=q)]
    response = dict(topic_list_with_keyword_in_question=topic_list_with_keyword_in_question,
                    topic_list_with_keyword_in_answer=topic_list_with_keyword_in_answer, category_list=category_list)

    return HttpResponse(json.dumps({'success': True, 'data': response}), 'content-type:text/json')