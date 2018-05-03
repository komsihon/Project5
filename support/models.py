from django.db import models
from datetime import datetime

from conf import settings
from ikwen.core.models import Application, Model
from ikwen.accesscontrol.models import Member
from django.utils.translation import gettext_lazy as _

ENGLISH = 'English'
FRENCH = 'Francais'

LANGUAGE_CHOICES = (
    (ENGLISH, 'English'),
    (FRENCH, 'Francais')
)


class Chapter(Model):
    title = models.CharField(max_length=240, blank=False, unique=True)
    language = models.CharField(max_length=30, choices=LANGUAGE_CHOICES, default=FRENCH)
    app = models.ForeignKey(Application)
    slug = models.SlugField(max_length=240, blank=False, unique=True)
    publish = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s - %s" % (self.title, self.app)


class Topic(Model):
    title = models.CharField(max_length=240, blank=False, unique=True)
    language = models.CharField(max_length=30, choices=LANGUAGE_CHOICES, default=FRENCH)
    summary = models.CharField(max_length=255,
                               help_text=_("Few words to words to let the user knows what you a going to say"))
    slug = models.SlugField(max_length=240, blank=False, unique=True)
    content = models.TextField(blank=True, null=True, help_text=_("Full text describing the topic"))
    # entry = models.TextField(blank=True, null=True, help_text=_("Full text describing the topic"))
    chapter = models.ForeignKey(Chapter,
                                help_text=_("Chapter where this topic belongs to"))
    pub_date = models.DateField(default=datetime.now)
    tags = models.CharField(max_length=255, blank=True,
                            help_text=_("Few space-separated keywords to find the sub-chapter"))
    member = models.ForeignKey(Member, blank=False, null=True,
                               help_text=_("Member who conceive and write the tutorial"))
    order_of_appearance = models.SmallIntegerField(default=1000)
    publish = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s - %s' % (self.title, self.chapter.app.name)

    def get_path(self):
        folders = '%s/%s' % (self.app.slug, self.slug)
        return '%s' % folders

    def get_uri(self):
        return '%s/%s/%s' % (settings.BASE_URI, self.chapter.app.slug, self.slug)

    def _get_app(self):
        return self.chapter.app
    app = property(_get_app)


class UserPointOfView(Model):
    YES = "Yes"
    NO = "No"
    PERTINENCE_CHOICES = (
        (YES, "Yes"),
        (NO, "No"),
    )
    topic = models.ForeignKey(Topic)
    pertinence = models.CharField(max_length=15, choices=PERTINENCE_CHOICES, default=YES)
    comment = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=240, null=True, blank=True)