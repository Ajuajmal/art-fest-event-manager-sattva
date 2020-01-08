from django import forms
from .models import Participant
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class Participant(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('event', 'name', 'regnumber','contact', 'sem', 'branch',)
