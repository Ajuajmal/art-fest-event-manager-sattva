from django.contrib import admin

from .mixins import ExportCsvMixin

from .models import Participant,Event,Category


class EventAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ('name', 'max_participants')
    list_filter = ('max_participants',)
    prepopulated_fields = {'slug':('name',)}
    actions = ["export_as_csv","update_event_withdrawn","update_event_draft","update_event_finsh"]
    def update_event_finsh(self, request, queryset):
        queryset.update(venue=3)
    def update_event_withdrawn(self, request, queryset):
        queryset.update(venue=2)
    def update_event_draft(self, request, queryset):
        queryset.update(venue=1)
    update_event_draft.allowed_permissions = ('change',)
    update_event_finsh.allowed_permissions = ('change',)
    update_event_withdrawn.allowed_permissions = ('change',)




class ParticipantAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'branch','event','payment','deletable','slot')
    list_filter = ('event','branch','regnumber',)
    search_fields = ['name', 'regnumber', 'event']
    actions = ["export_as_csv","update_payment_complete","update_payment_incomplete","update_delete_false","update_delete_true"]
    def update_payment_complete(self, request, queryset):
        queryset.update(payment=True)
    def update_payment_incomplete(self, request, queryset):
        queryset.update(payment=False)
    update_payment_complete.allowed_permissions = ('change',)
    update_payment_incomplete.allowed_permissions = ('change',)
    def update_delete_true(self, request, queryset):
        queryset.update(deletable=True)
    def update_delete_false(self, request, queryset):
        queryset.update(deletable=False)
    update_delete_true.allowed_permissions = ('change',)
    update_delete_false.allowed_permissions = ('change',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)




admin.site.register(Category,CategoryAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Event,EventAdmin)
