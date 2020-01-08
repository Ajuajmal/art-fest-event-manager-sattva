from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.views import generic
from django.utils import timezone

from django_tables2 import SingleTableView

from events.models import Participant
from .tables import ParticipantTable

@login_required
@transaction.atomic
def dashviews(request):
    return render(request, 'dashboard_base.html')



class ParticipantListView(SingleTableView):
    model = Participant
    table_class = ParticipantTable
    template_name = 'tables.html'

def person_list(request):
    table = ParticipantTable(Participant.objects.filter(branch=0))

    return render(request, "tables.html", {
        "table": table
    })
