from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.views import generic
from django.utils import timezone

from django_tables2 import SingleTableView,LazyPaginator
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from events.models import Participant
from .tables import ParticipantTable,ParticipantTableCapt,ParticipantTableAdmin


def dashviews(request):
    return render(request, 'dashboard_base.html')




class ParticipantListView(LoginRequiredMixin,SingleTableView):
    model = Participant
    table_class = ParticipantTable
    template_name = 'tables.html'
    paginator_class = LazyPaginator

@login_required
def participant_list(request):
    table = ParticipantTableCapt(Participant.objects.filter(branch=request.user.profile.branch).filter(deletable=False).order_by('event'))
    if request.user.is_staff:
        table = ParticipantTableAdmin(Participant.objects.filter(deletable=False).order_by('event'))
    return render(request, "captian_list.html", {
        "table": table
    })
def payment_list(request):
    table = ParticipantTable(Participant.objects.filter(branch__in=[0,1,2]).order_by('slot'))
    return render(request, "tables.html", {
        "table": table
    })
def payment_lists(request):
        table = Participant.objects.filter(branch = 0).order_by('slot').order_by('event')
        return render(request, "pay_table.html", {
                "table": table
            })
