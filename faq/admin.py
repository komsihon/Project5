from django.contrib import admin
# from faq.models import Topic, Category, Question, Topic1, Question1
from faq.models import Topic, Question
from ikwen.core.models import Application
from ikwen.core.admin import ApplicationAdmin


class TopicAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'app', 'language', 'base_lang_version')
    list_display = ('title', 'app', 'language', 'base_lang_version')


class QuestionAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("label",)}
    fields = ('label', 'tags', 'topic', 'user_views',
              'count_helpful', 'count_helpless', 'language', 'base_lang_version')
    list_display = ('label', 'tags', 'topic', 'user_views',
                    'count_helpful', 'count_helpless', 'author', 'language', 'base_lang_version')


admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Topic1, Topic1Admin)
# admin.site.register(Question1, Question1Admin)
# admin.site.register(Application, ApplicationAdmin)

