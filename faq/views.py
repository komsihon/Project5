import sys
import json
import re

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import get_language, gettext as _
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from ikwen.core.views import HybridListView, ChangeObjectBase
from ikwen.core.utils import to_dict

from faq.admin import TopicAdmin, QuestionAdmin
from faq.models import Application, Topic, Question

reload(sys)
sys.setdefaultencoding('utf-8') # Allow system to decode utf-8's strings such as ',",|,?


def create_sentence_with_keyword(paragraph, keyword_word):
    sentence_list = []
    for sentence in paragraph.split('.'):
        if keyword_word in sentence:
            sentence_list.append(sentence+".\n")
    return sentence_list


def clean_html(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


class Home(TemplateView):
    template_name = 'faq/home_faq.html'

    def get_context_data(self, **kwargs):
        language = get_language()
        context = super(Home, self).get_context_data(**kwargs)
        app_list = []
        # add_database(UMBRELLA)
        # for app in Application.objects.using(UMBRELLA).all().order_by('name'):
        # for app in get_object_or_404(Application).objects.order_by('name').all():
        for app in Application.objects.all().order_by('name'):
            topic_list = list(Topic.objects.filter(app=app, language=language))
            question_list = Question.objects.filter(topic__in=topic_list, language=language)
            if question_list.count() > 0:
                app.question_list = question_list
                app_list.append(app)

        context['app_list'] = app_list

        return context


class QuestionDetail(TemplateView):
    template_name = 'faq/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data()
        app_slug = kwargs['app_slug']
        topic_slug = kwargs['topic_slug']
        question_slug = kwargs['question_slug']
        topic = get_object_or_404(Topic, slug=topic_slug)
        question = get_object_or_404(Question, slug=question_slug)

        # add_database(UMBRELLA)
        app = get_object_or_404(Application, slug=app_slug)
        current_language = get_language()
        prev_lang = ''
        if question.language != current_language:
            prev_lang = question.language
        while topic.language != current_language:
            topic = topic.base_lang_version

        while question.language != current_language:
            if not question.base_lang_version:
                context['message'] = _('The question is not yet available in your selected language')
                break
            question = question.base_lang_version

        context['app'] = app
        context['topic'] = topic
        context['question'] = question

        return context

    def render_to_response(self, context, **response_kwargs):
        lang = get_language()
        topic = context['topic']
        question = context['question']
        if topic.language != lang:
            try:
                translated_topic = Topic.objects.get(language=lang, base_lang_version=topic.base_lang_version)
                translated_question = Question.objects.get(language=lang, base_lang_version=question.base_lang_version)
                next_url = reverse('faq:question_detail', args=(translated_topic.app.slug, translated_topic.slug,
                                                                translated_question.slug))
                return HttpResponseRedirect(next_url)
            except:
                pass
        return super(QuestionDetail, self).render_to_response(context, **response_kwargs)


class ShowTopicList(TemplateView):
    """
    written by: Silatchom SIAKA (AI responsible)
    """
    template_name = 'faq/show_topic_list.html'

    def get_context_data(self, **kwargs):
        context = super(ShowTopicList, self).get_context_data()
        app_slug = kwargs['app_slug']
        language = get_language()
        topic_list = []
        app = get_object_or_404(Application, slug=app_slug)
        for topic in Topic.objects.filter(language=language, app=app).order_by('title'):
            question_list = []
            for question in Question.objects.filter(topic=topic, language=language):
                question_list.append(question)
            topic.question_list = question_list
            topic_list.append(topic)
        context['topic_list'] = topic_list
        context['app'] = app
        return context


class ShowQuestionList(TemplateView):
    """
    """
    template_name = 'faq/question_list.html'

    def get_context_data(self, **kwargs):
        language = get_language()
        context = super(ShowQuestionList, self).get_context_data()
        q = self.request.GET["q"]
        tag_list = []

        for word in q.split(' '):
            tag_list.append(word[:4])

        tag_list.sort()
        tags = ' '.join(tag_list)
        topic_list = list(Topic.objects.filter(title__icontains=tags, language=language))
        question_list_1 = list(Question.objects.filter(label__icontains=tags, language=language))

        # question_list_2 = []
        # for question in Question.objects.filter(language=language):
        #     if question not in question_list_1:
        #         if q not in topic_list:
        #             question.sentence_with_keyword = create_sentence_with_keyword(question.answer, q)
        #             # question.sentence_with_keyword = create_sentence_with_keyword(clean_html(question.answer), q)
        #             if len(question.sentence_with_keyword) > 0:
        #                 question_list_2.append(question)

        context['question_list_1'] = question_list_1
        # context['question_list_2'] = question_list_2
        context['topic_list'] = topic_list
        context['q'] = q
        return context


def save_user_feedback(request, *args, **kwargs):
    language = get_language()
    q = request.GET
    question = q.get('q')
    matched_question = Question.objects.get(language=language, slug=question)
    count_helpful = q.get('count_helpful')
    count_helpless = q.get('count_helpless')
    user_views = q.get('user_views')
    if user_views:
        matched_question.user_views += int(user_views)
    if count_helpless or count_helpful:
        matched_question.count_helpful += int(count_helpful)
        matched_question.count_helpless += int(count_helpless)
    matched_question.save()
    response = "Successfully receive the request"
    return HttpResponse(json.dumps({'success': True, 'count_helpful': matched_question.count_helpful}),
                        'content-type: text/json')


def autocomplete_user_research(request, *args, **kwargs):
    language = get_language()
    q = request.GET['q']
    question_list_with_keyword_in_label = []
    question_list_with_keyword_in_answer = []

    for question in Question.objects.filter(language=language):
        if q not in [topic.title for topic in Topic.objects.filter(title__icontains=q)]:
            if q in question:
                question_list_with_keyword_in_label.append(to_dict(question))
            else:
                question.sentence_with_keyword = create_sentence_with_keyword(question.answer, q)
                # question.sentence_with_keyword = create_sentence_with_keyword(clean(question.answer), q)
                if len(question.sentence_with_keyword) > 0:
                    question_list_with_keyword_in_answer.append(to_dict(question))

    topic_list = [to_dict(obj) for obj in Topic.objects.filter(title__icontains=q)]
    response = dict(question_list_with_keyword_in_label=question_list_with_keyword_in_label,
                    question_list_with_keyword_in_answer=question_list_with_keyword_in_answer, topic_list=topic_list)

    return HttpResponse(json.dumps({'success': True, 'data': response}), 'content-type:text/json')


class TopicList(HybridListView):
    """
    Here is the admin topic list view.
    """
    model = Topic
    ordering = ('title',)
    search_field = 'title'
    list_filter = ('language', 'app',)


class QuestionList(HybridListView):
    """
    Here is the admin question list view.
    """
    model = Question
    search_field = 'label'
    list_filter = ('label', 'language', 'topic', 'user_views', 'count_helpful', 'count_helpless')


class ChangeTopic(ChangeObjectBase):
    model = Topic
    model_admin = TopicAdmin
    label_field = 'title'


class ChangeQuestion(ChangeObjectBase):
    model = Question
    model_admin = QuestionAdmin
    label_field = 'label'


