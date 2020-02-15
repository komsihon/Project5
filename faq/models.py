from django.conf import settings
from django.db import models
from ikwen.accesscontrol.backends import UMBRELLA
from ikwen.core.models import Application, Model
from ikwen.accesscontrol.models import Member
from django.template.defaultfilters import slugify


class Topic(Model):
    """
    Topic field which replaces category model in the previous modeling
    """
    title = models.CharField(max_length=100, null=True, blank=True)  # type: unicode
    slug = models.SlugField(max_length=250, null=True, blank=True)
    app = models.ForeignKey(Application, null=True, blank=True)
    language = models.CharField(max_length=2, choices=getattr(settings, "LANGUAGES"), null=True, blank=True)
    base_lang_version = models.ForeignKey('self', null=True, blank=True)
    order_of_appearance = models.IntegerField(default=0)

    class Meta:
        unique_together = (
            ('app', 'title'),
            ('app', 'slug')
        )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Topic, self).save()


class Question(Model):
    """
    Question field which replaces Topic model in the previous modeling
    """
    admin = Member.objects.get(username__icontains='siaka')
    label = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=240)
    tags = models.CharField(null=True, blank=True)
    answer = models.TextField(blank=True)
    topic = models.ForeignKey(Topic, null=True, blank=True)
    user_views = models.IntegerField(default=0)
    count_helpful = models.IntegerField(default=0)
    count_helpless = models.IntegerField(default=0)
    author = models.ForeignKey(Member, null=True, editable=False,  default=admin.id)
    language = models.CharField(max_length=2, choices=getattr(settings, "LANGUAGES"), null=True, blank=True)
    base_lang_version = models.ForeignKey('self', null=True, blank=True)
    order_of_appearance = models.IntegerField(default=0)

    class Meta:
        unique_together = (
            ('topic', 'label'),
            ('topic', 'slug')
        )

    def __unicode__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.label)
        super(Question, self).save()







