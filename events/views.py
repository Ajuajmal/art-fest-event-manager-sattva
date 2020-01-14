from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

def homeviews(request):
    return render(request, 'home.html')



class ParticipantCreateView(SuccessMessageMixin,LoginRequiredMixin, CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'participant_form.html'
    success_url = reverse_lazy('newregistration')
    success_message = "%(event)s registration for %(name)s  was successfully Processed"
    def form_valid(self, form):
        form.instance.branch = self.request.user.profile.branch
        return super(ParticipantCreateView, self).form_valid(form)
@login_required
@transaction.atomic
def newreg(request):
    user = get_object_or_404(User, username=username)
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
    return render(request, 'participant_form.html', {'form': form, 'user': user})

def participant_list(request):
    participants = Participant.objects.filter(branch=request.user.profile.branch).filter(deletable=True)
    return render(request, 'participant_list.html', {'participants': participants})

def save_participant_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            participants = Participant.objects.all()
            data['html_participant_list'] = render_to_string('partial_participant_list.html', {
                'participants': participants
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
    else:
        form = ParticipantForm(instance=participant)
    return save_participant_form(request,form ,'participant_update.html')

def load_events(request):
    category_id = request.GET.get('category')
    events = Event.objects.filter(category_id=category_id).filter(venue=1).order_by('name')
    return render(request, 'event_dropdown_list_options.html', {'events': events})

def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    data = dict()
    if request.method == 'POST':
        participant.delete()
        data['form_is_valid'] = True
        participants = Participant.objects.all()
        data['html_participant_list'] = render_to_string('participant_list.html', {
            'participants': participants
        })
        print(data)
    else:
        context = {'participant': participant}
        data['html_form'] = render_to_string('partial_participant_delete.html', context, request=request)
        print(data)
    return JsonResponse(data)
