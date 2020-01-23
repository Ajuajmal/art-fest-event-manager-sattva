import django_tables2 as tables
from events.models import Participant
from django_tables2.export.export import TableExport


class ParticipantTable(tables.Table):
    export_formats = ['csv', 'xlsx']
    class Meta:
        model = Participant
        template_name = "django_tables2/bootstrap.html"
        fields = ("name",'event','slot','payment','semester','regnumber' )
class ParticipantExportTable(tables.Table):
    export_formats = ['csv', 'xlsx']
    class Meta:
        model = Participant
        template_name = "django_tables2/bootstrap.html"
        fields = ("no","lot","name",'event','slot','branch','semester','regnumber' )
class ParticipantTableCapt(tables.Table):
    class Meta:
        model = Participant
        template_name = "django_tables2/bootstrap.html"
        fields = ("name",'semester','participant_type','event','slot','payment' )

class ParticipantTableAdmin(tables.Table):
    class Meta:
        model = Participant
        template_name = "django_tables2/bootstrap.html"
        fields = ("name",'branch','semester','participant_type','event','slot','payment' )
