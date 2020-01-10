from django import forms
from .models import Participant,Event,Category
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('category','event', 'name', 'regnumber','contact', 'semester', 'branch',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].queryset = Event.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['event'].queryset = Event.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['event'].queryset = self.instance.category.event_set.order_by('name')
