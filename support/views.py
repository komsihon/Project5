from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
import os
# Create your views here.
from django.views.generic.base import TemplateView

from conf import settings
from support.models import Application, Chapter, SubChapter, UserPointOfView
from django.http import HttpResponse
import json
from ikwen.core.models import Application

POST_PER_PAGE = 8

MEDIA_DIR = settings.MEDIA_ROOT + 'tiny_mce/'
TINYMCE_MEDIA_URL = settings.MEDIA_URL + 'tiny_mce/'


class SupportList(TemplateView):
    template_name = 'support/home.html'

    def get_context_data(self, **kwargs):
        context = super(SupportList, self).get_context_data(**kwargs)
        support_list = Application.objects.all()
        context['support_list'] = support_list
        return context


class TopicList(TemplateView):
    template_name = 'support/app_table_of_contents.html'

    def get_context_data(self, **kwargs):
        context = super(TopicList, self).get_context_data(**kwargs)
        application_slug = kwargs['application_slug']
        application = Application.objects.get(slug=application_slug)
        chapters = Chapter.objects.filter(app=application, publish=True)
        sub_chap = []
        for chapter in chapters:
            c = SubChapter.objects.filter(chapter=chapter)
            if c.count() > 0:
                c.chapter = chapter
                sub_chap.append(c)
        # sub_chapters = SubChapter.objects.filter(chapter__in=chapters).order_by('order_of_appearance')
        # sub_chapters = SubChapter.objects.filter(chapter__in=chapters).order_by('chapter')
        context['chapters'] = sub_chap
        context['application'] = application
        return context


class SupportDetails(TemplateView):
    template_name = 'support/tuto_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SupportDetails, self).get_context_data(**kwargs)
        application_slug = kwargs['application_slug']
        slug = kwargs['sub_chapter_slug']
        application = Application.objects.get(slug=application_slug)
        chapters = Chapter.objects.filter(app=application, publish=True)
        sub_chap = []
        for chapter in chapters:
            c = SubChapter.objects.filter(chapter=chapter)
            if c.count() > 0:
                c.chapter = chapter
                sub_chap.append(c)
        sub_chapter = get_object_or_404(SubChapter, slug=slug)
        context['current_sub_chapter'] = sub_chapter
        context['chapters'] = chapters
        context['sub_chapter'] = sub_chap
        context['sibling_sub_chapter'] = SubChapter.objects.filter(chapter=sub_chapter.chapter)
        return context


class AdminHome(TemplateView):
    template_name = 'support/admin_home.html'


class Search(TemplateView):
    template_name = 'support/search.html'

    # def get_context_data(self, **kwargs):
    #     context = super(Search, self).get_context_data(**kwargs)
    #     application_slug = kwargs['application_slug']
    #     radix = self.request.GET.get('radix')
    #     if radix == '':
    #         radix = "No-radix"
    #     application = Application.objects.get(slug=application_slug)
    #
    #     entries = grab_items_by_radix(application, radix)
    #     context['pages'] = get_paginated_view(self.request, entries, POST_PER_PAGE)
    #     context['entries'] = entries
    #     return context


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


def save_pertinence(request, *args, **kwarg):
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
    article = get_object_or_404(SubChapter, pk=article_id)
    user_point_of_view = UserPointOfView(author=author, pertinence=pertinence, comment=comment, article=article)
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
