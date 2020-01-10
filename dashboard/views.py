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
    paginator_class = LazyPaginator

def person_list(request):
    table = ParticipantTable(Participant.objects.filter(branch__in=[0,1,2,3,4,5]).group_by('-name'))
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    return render(request, "tables.html", {
        "table": table
    })
