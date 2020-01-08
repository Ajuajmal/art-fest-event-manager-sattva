from django import forms
from .models import Participant
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('event', 'name', 'regnumber','contact', 'semester', 'branch',)
