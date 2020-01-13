from django.contrib import admin

from .mixins import ExportCsvMixin

from .models import Participant,Event,Category


class EventAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ('name', 'max_participants')
    list_filter = ('max_participants',)
    prepopulated_fields = {'slug':('name',)}
    actions = ["export_as_csv"]


class ParticipantAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'branch','event','payment')
    list_filter = ('event','regnumber','branch')
    search_fields = ['name', 'regnumber', 'event']
    actions = ["export_as_csv"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)




admin.site.register(Category,CategoryAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Event,EventAdmin)
