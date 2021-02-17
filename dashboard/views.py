from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import PresenceFile

# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html')

def presence(request):
    latest_presence_files = PresenceFile.objects.order_by('-upload_date')[:50]
    context = {'latest_presence_files': latest_presence_files}
    return render(request, 'dashboard/presence.html', context)