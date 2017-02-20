from django.contrib import admin

from schedule.models import Calendar, Event, CalendarRelation, \
    Rule, PurchaseCourse
from schedule.forms import EventAdminForm


class CalendarAdminOptions(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ("id", "user", "coach", "start", "end", "calendar")


class PurchaseCourseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "remain")


admin.site.register(Calendar, CalendarAdminOptions)
admin.site.register(Event, EventAdmin)
admin.site.register(PurchaseCourse, PurchaseCourseAdmin)
admin.site.register([Rule, CalendarRelation])
