import django_tables2 as tables
from events.models import Participant

class ParticipantTable(tables.Table):
    class Meta:
        model = Participant
        template_name = "django_tables2/bootstrap.html"
        fields = ("name",'branch','event','contact','payment' )
