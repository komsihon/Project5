# -*- coding: utf-8 -*-
from django.contrib import admin
from ikwen.accesscontrol.admin import MemberAdmin
from ikwen.accesscontrol.models import Member
from ikwen.billing.models import Invoice, Product, Subscription, Payment, PaymentMean, MoMoTransaction, CloudBillingPlan
from ikwen.core.models import ConsoleEvent, Service
from ikwen.theming.models import Theme, Template

from support.models import Chapter, SubChapter


class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'app', 'publish')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', )
    list_filter = ('app', 'publish')


class SubChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'member', 'publish')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', )
    list_filter = ('chapter', 'member', 'publish')
    readonly_fields = ('pub_date', 'member')

    def save_model(self, request, obj, form, change):
        obj.member = request.user
        super(SubChapterAdmin, self).save_model(request, obj, form, change)


admin.site.unregister(Invoice)
admin.site.unregister(Product)
admin.site.unregister(Subscription)
# admin.site.unregister(PaymentMean)
# admin.site.unregister(MoMoTransaction)
# admin.site.unregister(Payment)
# admin.site.unregister(CloudBillingPlan)

# admin.site.unregister(ConsoleEvent)
# admin.site.unregister(Service)
# admin.site.unregister(Theme)
# admin.site.unregister(Template)
# admin.site.unregister(Member)

admin.site.register(Chapter, ChapterAdmin)
admin.site.register(SubChapter, SubChapterAdmin)
admin.site.register(Member, MemberAdmin)