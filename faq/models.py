from django.db import models
from ikwen.core.models import Application, Model
from ikwen.accesscontrol.models import Member
from django.template.defaultfilters import slugify
LANGUAGES = (
        ('EN', 'English'),
        ('FR', 'French'),
    )


class Question(Model):
    text = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=150, blank=False, unique=True)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    translated_versions = models.ForeignKey('self', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.text)
        super(Question, self).save()

    def __unicode__(self):
        return self.text


class Category(Model):
    name = models.CharField(max_length=100, null=False, blank=True)  # type: unicode
    app = models.ForeignKey(Application)
    slug = models.SlugField(max_length=250, blank=False, unique=True)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    translated_versions = models.ForeignKey('self', null=True, blank=True)
    order_of_appearance = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save()


class Topic(Model):
    """
    doc
    """
    question = models.OneToOneField(Question, null=False, blank=True)
    slug = models.SlugField(max_length=240, blank=False, unique=True)
    answer = models.TextField()
    answer_with_html_tags = models.TextField(blank=True)
    category = models.ForeignKey(Category)
    user_views = models.IntegerField(default=0)
    count_helpful = models.IntegerField(default=0)
    count_helpless = models.IntegerField(default=0)
    author = models.ForeignKey(Member)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    translated_versions = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.slug

    def get_question_text(self):
        return self.question.text

# from faq.utils import unique_slug_generator


# def Post(models.Model):
#     title = models.CharField(max_length=150)
#     body = models.TextField()
#
#     def __str__(self):
#         return self.title
#
#     def slug_save(sender, instance, *args, **kwargs):
#         if not instance.slug:
#             instance.slug = unique_slug_generator(instance, instance.title, instance.body)
#
# pre_save.connect(slug_save, sender=Post)



