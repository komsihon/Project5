from django.contrib import admin
from faq.models import Topic, Category, Question


# class TsunamiPageAdmin(admin.ModelAdmin):
#     fields = ('name', 'page_title', 'faq_category', 'question_type', 'header', 'content')
#
#
# class TsunamiPageAdmin(admin.ModelAdmin):
#     exclude = ('slug',)


class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("text",)}
    list_display = ('text', 'slug',)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', 'app')


class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("question",)}
    # list_display = ('question', 'slug', 'answer', 'category', 'views', 'count_helpful', 'count_helpless', 'author')


admin.site.register(Topic, TopicAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
