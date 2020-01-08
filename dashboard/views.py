from django.shortcuts import render

# Create your views here.
def dashviews(request):
    return render(request, 'dashboard_base.html')
