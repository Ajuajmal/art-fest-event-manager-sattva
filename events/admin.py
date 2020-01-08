from django.contrib import admin

from .models import Participant,Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_participants')
    list_filter = ('max_participants',)
    prepopulated_fields = {'slug':('name',)}


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'contact','payment')
    list_filter = ('event','regnumber','branch')
    search_fields = ['name', 'regnumber', 'event']





admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Event,EventAdmin)
