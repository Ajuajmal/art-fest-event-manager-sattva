from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.views import generic
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import ParticipantForm
from .models import Participant,Event

def homeviews(request):
    return render(request, 'home.html')



class ParticipantCreateView(CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'participant_form.html'
    success_url = reverse_lazy('newregistration')
@login_required
@transaction.atomic
def newreg(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your Registraion Processed Successfully')
            return redirect('newregistration')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ParticipantForm()
    return render(request, 'participant_form.html', {'form': form})

def load_events(request):
    category_id = request.GET.get('category')
    events = Event.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'event_dropdown_list_options.html', {'events': events})
