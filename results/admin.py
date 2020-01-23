from django.contrib import admin

# Register your models here.
from django.contrib import admin

from events.mixins import ExportCsvMixin

from .models import EventsResult,BranchPoint
class EventsResultsAdmin(admin.ModelAdmin):
    list_display = ('event',)


class BranchPointAdmin(admin.ModelAdmin):
    list_display = ('event','branch','score')
admin.site.register(EventsResult,EventsResultsAdmin)

admin.site.register(BranchPoint,BranchPointAdmin)
