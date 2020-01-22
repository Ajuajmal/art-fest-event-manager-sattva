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
from events.models import Participant,Event
from .tables import ParticipantTable,ParticipantTableCapt,ParticipantTableAdmin
from results.models import BranchPoint
from django_filters.views import FilterView

import django_filters

class ParticipantFilter(django_filters.FilterSet):

    class Meta:
        model = Participant
        fields = ['event','regnumber']

def dashviews(request):
        score = BranchPoint.objects.all()
        ce =0
        cse = 0
        ec = 0
        eee = 0
        it = 0
        me = 0
        me = 0
        mca = 0
        cetime=csetime=ectime=eeetime=ittime=metime=mcatime=timezone.now()
        for x in score :
            if x.branch == 0:
                ce +=x.score
                cetime = x.updated_on
            if x.branch == 1:
                cse +=x.score
                csetime = x.updated_on
            if x.branch == 2:
                ec +=x.score
                ectime = x.updated_on
            if x.branch == 3:
                eee +=x.score
                eeetime = x.updated_on
            if x.branch == 4:
                it +=x.score
                ittime = x.updated_on
            if x.branch == 5:
                me +=x.score
                metime = x.updated_on
            if x.branch == 6:
                mca +=x.score
                mcatime = x.updated_on
        return render(request, 'dashboard_base.html',{
    "ce": ce,"cetime":cetime,
    "cse": cse,"csetime":csetime,
    "ec": ec,"ectime":ectime,
    "eee": eee,"eeetime":eeetime,
    "it": it,"ittime":ittime,
    "me": me,"metime":metime,
    "mca": mca,"mcatime":mcatime})






class ParticipantListView(LoginRequiredMixin,SingleTableMixin,FilterView):
    model = Participant
    table_class = ParticipantTable
    template_name = 'tables.html'
    paginator_class = LazyPaginator

    filterset_class = ParticipantFilter
    def get_queryset(self):
        if self.request.user.is_staff:
            return Participant.objects.all()
        else:
            return Participant.objects.filter(branch=self.request.user.profile.branch)

@login_required
def participant_list(request):
    events = Event.objects.filter(venue__in =[1,2])
    table = ParticipantTableCapt(Participant.objects.filter(branch=request.user.profile.branch).filter(event__in=events).order_by('event'))
    if request.user.is_staff:
        table = ParticipantTableAdmin(Participant.objects.order_by('event'))
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
