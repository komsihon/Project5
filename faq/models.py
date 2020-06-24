from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from ikwen.accesscontrol.backends import UMBRELLA

from ikwen.core.models import Application, Model
from ikwen.accesscontrol.models import Member


class Topic(Model):
    """
    Topic field which replaces category model in the previous modeling
    """
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Title'))  # type: unicode
    slug = models.SlugField(max_length=250, null=True, blank=True)
    app = models.ForeignKey(Application, null=True, blank=True, verbose_name=_('Application'))
    language = models.CharField(max_length=2, choices=getattr(settings, "LANGUAGES"), null=True, blank=True, verbose_name=_('Language'))
    base_lang_version = models.ForeignKey('self', null=True, blank=True, verbose_name=_('Base language version'))
    order_of_appearance = models.IntegerField(default=0, verbose_name=_('Order of appearance'))
    summary = models.TextField(blank=True, null=True, verbose_name=_('Summary'))

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
    label = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Label'))
    slug = models.SlugField(max_length=240)
    tags = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Tags'))
    answer = models.TextField(blank=True, verbose_name=_('Answer'))
    topic = models.ForeignKey(Topic, null=True, blank=True, verbose_name=_('Topic'))
    user_views = models.IntegerField(default=0, verbose_name=_('User views'))
    count_helpful = models.IntegerField(default=0, verbose_name=_('Count helpful'))
    count_helpless = models.IntegerField(default=0, verbose_name=_('Count helpless'))
    author = models.ForeignKey(Member, null=True, editable=False,  default=admin.id, verbose_name=_('Author'))
    language = models.CharField(max_length=2, choices=getattr(settings, "LANGUAGES"), null=True, blank=True, verbose_name=_('Language'))
    base_lang_version = models.ForeignKey('self', null=True, blank=True, verbose_name=_('Base language version'))
    order_of_appearance = models.IntegerField(default=0, verbose_name=_('Order of appearance'))
    appear_on_home = models.BooleanField(default=False, verbose_name=_('Appear on home'))
    summary = models.TextField(blank=True, null=True, verbose_name=_('Summary'))

    class Meta:
        unique_together = (
            ('topic', 'label'),
            ('topic', 'slug')
        )
        ordering = ('label', )

    def __unicode__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.label)
        tag_list = [tag[:4] for tag in self.slug.split('-')]
        tag_list.sort()
        self.tags = ' '.join(tag_list)
        if self.base_lang_version:
            self.topic.default = self.base_lang_version
        else:
            self.topic.default = Topic.objects.filter(title__icontains=self.label).first()
        super(Question, self).save()







