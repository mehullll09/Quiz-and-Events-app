from django.shortcuts import render
from .models import*

# Create your views here.

def event_list(request):
    events = Event.objects.all()
    con = {'events': events}
    return render(request, 'events.html', con)