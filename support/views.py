from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
import os
# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.utils import translation

from conf import settings
from support.models import Application, Chapter, Topic, UserPointOfView
from django.http import HttpResponse
import json
from ikwen.core.models import Application


ENGLISH = 'English'
FRENCH = 'Francais'

LANGUAGE_CHOICES = (
    (ENGLISH, 'English'),
    (FRENCH, 'Francais')
)

POST_PER_PAGE = 8

MEDIA_DIR = settings.MEDIA_ROOT + 'tiny_mce/'
TINYMCE_MEDIA_URL = settings.MEDIA_URL + 'tiny_mce/'


class Home(TemplateView):
    template_name = 'support/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        support_list = Application.objects.all()
        for support in support_list:
            support.chapter_count = Chapter.objects.filter(app=support, publish=True).count()
            if support.chapter_count == 1:
                chapter = Chapter.objects.filter(app=support, publish=True)[0]
                support.topic = Topic.objects.filter(chapter=chapter, publish=True)[0]
        context['support_list'] = support_list
        return context


class TopicList(ListView):
    template_name = 'support/topic_list.html'
    context_object_name = 'chapter_queryset'
    model = Chapter

    def get_context_data(self, **kwargs):
        context = super(TopicList, self).get_context_data(**kwargs)
        lang = translation.get_language()
        if 'en' in lang:
            language = ENGLISH
        else:
            language = FRENCH
        application_slug = kwargs['application_slug']
        application = Application.objects.get(slug=application_slug)
        context['application'] = application
        # context[self.get_context_object_name(self.object_list)] = Chapter.objects.filter(app=application,
        #  language=language, publish=True)
        context[self.get_context_object_name(self.object_list)] = Chapter.objects.filter(app=application, publish=True)
        return context


class TopicDetail(TemplateView):
    template_name = 'support/topic_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TopicDetail, self).get_context_data(**kwargs)
        lang = translation.get_language()
        if 'en' in lang:
            language = ENGLISH
        else:
            language = FRENCH
        application_slug = kwargs['application_slug']
        topic_slug = kwargs['topic_slug']
        app = Application.objects.get(slug=application_slug)
        chapter_list = Chapter.objects.filter(app=app, publish=True)
        # chapter_list = Chapter.objects.filter(app=app, language=language, publish=True)
        # topic = get_object_or_404(Topic, slug=topic_slug, language=language)
        topic = get_object_or_404(Topic, slug=topic_slug)
        context['chapter_list'] = chapter_list
        context['topic'] = topic
        return context


class AdminHome(TemplateView):
    template_name = 'support/admin_home.html'


class Search(TemplateView):
    template_name = 'support/search.html'


def get_paginated_view(rq, items, nos):
    items_paginated = False
    paginator = Paginator(items, nos)
    page = rq.GET.get('page')
    try:
        items_paginated = paginator.page(page)
    except PageNotAnInteger:
        items_paginated = paginator.page(1)
    except EmptyPage:
        items_paginated = paginator.page(paginator.num_pages)
    return items_paginated


def grab_items_by_radix(application, radix):
    items = []
    if radix is not None:
        radix.split(' ')
        posts = Application.objects.filter(title__icontains=radix, publish=True, app=application)
    else:
        posts = Application.objects.filter(publish=True, app=application)

    items.extend([post for post in posts])
    return items


def submit_review(request, *args, **kwarg):
    author = request.GET.get("author")
    pertinence = request.GET.get("pertinence")
    if pertinence == 'yes':
        pertinence = UserPointOfView.YES
    else:
        pertinence = UserPointOfView.NO
    comment = request.GET.get("comment")
    article_id = request.GET.get("article_id")
    if not pertinence or not article_id:
        return HttpResponse(
            json.dumps({'error': "An error occured"}),
            content_type='application/json'
        )
    article = get_object_or_404(Topic, pk=article_id)
    user_point_of_view = UserPointOfView(author=author, pertinence=pertinence, comment=comment, topic=article)
    user_point_of_view.save()
    if pertinence == UserPointOfView.YES:
        return HttpResponse(
            json.dumps({'success': True, 'message': "Thanks for your contribution"}),
            content_type='application/json'
        )
    else:
        return HttpResponse(
            json.dumps({'success': True, 'message': "Thanks for your contribution for better amelioration"}),
            content_type='application/json'
        )


def get_media(request, *args, **kwargs):
    media_list = []
    for root, dirs, files in os.walk(MEDIA_DIR):
        for filename in files:
            if filename.lower():
                filename = TINYMCE_MEDIA_URL + filename
                media_list.append(os.path.join(filename))
    response = {
        'media_list': media_list,
    }
    return HttpResponse(
        json.dumps(response),
        'content-type: text/json',
        **kwargs
    )


def delete_photo(request, *args, **kwargs):
    filename = request.GET.get('filename')
    file_path = ''
    if filename:
        file_path = filename.replace(settings.MEDIA_URL, settings.MEDIA_ROOT)
    try:
        os.remove(file_path)
        return HttpResponse(
            json.dumps({'success': True}),
            content_type='application/json'
        )
    except:
        response = "Error: %s file not found" % filename
        return HttpResponse(
            json.dumps({'error': response}),
            content_type='application/json'
        )
