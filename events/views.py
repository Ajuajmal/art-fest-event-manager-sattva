from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.views import generic
from django.utils import timezone

from .forms import ParticipantForm

def homeviews(request):
    return render(request, 'home.html')

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
    return render(request, 'newregistration.html', {'form': form})
