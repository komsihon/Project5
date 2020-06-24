from django.contrib import admin
# from faq.models import Topic, Category, Question, Topic1, Question1
from django.shortcuts import get_object_or_404

from faq.models import Topic, Question
from ikwen.core.models import Application
from ikwen.core.admin import ApplicationAdmin
from django.utils.translation import gettext as _


class TopicAdmin(admin.ModelAdmin):
    list_filter = ('app', 'language')
    fields = ('title', 'app', 'language', 'base_lang_version', 'order_of_appearance', 'summary')
    list_display = ('title', 'app', 'language', 'base_lang_version')


class ApplicationListFilter(admin.SimpleListFilter):
    title = _('application')
    parameter_name = 'application'

    def lookups(self, request, model_admin):
        """
        :param request:
        :param model_admin:
        :return:
        """
        result = []
        for q in Application.objects.all():
            result.append((q.id, q.name))
        return result

    def queryset(self, request, queryset):
        if self.value():
            app = Application.objects.get(pk=self.value())
            topic_list = list(Topic.objects.filter(app=app))
            return queryset.filter(topic__in=topic_list)


class QuestionAdmin(admin.ModelAdmin):
    list_filter = (ApplicationListFilter, 'topic', 'language')
    fields = ('label', 'topic', 'answer',
              'language', 'base_lang_version', 'appear_on_home', 'order_of_appearance', 'summary')
    list_display = ('label', 'tags', 'topic', 'user_views',
                    'count_helpful', 'count_helpless', 'language', 'base_lang_version')


admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)

