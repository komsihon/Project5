from django.db import models
from datetime import datetime
# Create your models here.
from django.utils import translation

from conf import settings
from ikwen.core.models import Application, Model
from ikwen.accesscontrol.models import Member
from ikwen.core.utils import to_dict
from django.utils.translation import gettext_lazy as _


def to_display_date(a_datetime):
    now = datetime.now()
    if translation.get_language().lower().find('en') == 0:
        now_date = '%02d/%02d, %d' % (now.month, now.day, now.year)
        display_date = '%02d/%02d, %d %02d:%02d' % (
            a_datetime.month, a_datetime.day, a_datetime.year,
            a_datetime.hour, a_datetime.minute
        )
        display_date = display_date.replace(now_date, '').strip()
    else:
        now_date = '%02d/%02d/%d' % (now.day, now.month, now.year)
        display_date = '%02d/%02d/%d %02d:%02d' % (
            a_datetime.day, a_datetime.month, a_datetime.year,
            a_datetime.hour, a_datetime.minute
        )
        display_date = display_date.replace(now_date, '').strip()
    return display_date

#
# class Application(Model):
#     app = models.ForeignKey(Application, blank=True, null=True)
#     summary = models.CharField(max_length=255)
#     media_link = models.URLField(blank=True, null=True)
#     pub_date = models.DateField(default=datetime.now)
#     footer_caption = models.CharField(max_length=250, blank=True)
#     tags = models.CharField(max_length=255, blank=True)
#     publish = models.BooleanField(default=False)
#
#     def __unicode__(self):
#         return "%s" % self.app.name
#
#     def get_path(self):
#         folders = '%s/%s/' % (self.app, self.slug)
#         return '%s' % folders
#
#     def get_uri(self):
#         return '%s%s' % (settings.BASE_URI, self.get_path())
#
#     def get_image_url(self):
#         if self.media:
#             return self.media.url
#         else:
#             return self.get_photo_placeholder()


class Chapter(Model):
    title = models.CharField(max_length=240, blank=False, unique=True)
    app = models.ForeignKey(Application)
    slug = models.SlugField(max_length=240, blank=False, unique=True)
    publish = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s - %s" % (self.title, self.app)


class SubChapter(Model):
    title = models.CharField(max_length=240, blank=False, unique=True)
    summary = models.CharField(max_length=255,
                               help_text=_("Few words to words to let the user knows what you a going to say"))
    slug = models.SlugField(max_length=240, blank=False, unique=True)
    content = models.TextField(blank=True, null=True,
                             help_text=_("Full text describing the subchapter"))
    chapter = models.ForeignKey(Chapter,
                                help_text=_("Chapter where this subchapter belongs to"))
    pub_date = models.DateField(default=datetime.now)
    tags = models.CharField(max_length=255, blank=True,
                            help_text=_("Few space-separated keywords to find the sub-chapter"))
    member = models.ForeignKey(Member, blank=False, null=True,
                               help_text=_("Member who conceive and write the tutorial"))
    order_of_appearance = models.SmallIntegerField(default=1000)
    publish = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s - %s" % (self.title, self.chapter.app.name)

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
    article = models.ForeignKey(SubChapter)
    pertinence = models.CharField(max_length=15, choices=PERTINENCE_CHOICES, default=YES)
    comment = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=240, null=True, blank=True)