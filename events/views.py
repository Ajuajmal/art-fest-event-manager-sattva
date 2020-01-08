from django.shortcuts import render, redirect
from django.views import generic


def homeviews(request):
    return render(request, 'home.html')
