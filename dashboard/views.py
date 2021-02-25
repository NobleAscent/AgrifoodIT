from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import PresenceFile


# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html')


def presence(request):
    latest_presence_files = PresenceFile.objects.order_by('-upload_date')[:50]
    context = {'latest_presence_files': latest_presence_files}
    return render(request, 'dashboard/presence.html', context)


def presence_upload(request):
    if request.method == 'POST':
        text_file = request.FILES.get('file')
        PresenceFile.objects.create(file_name='test123', processing_status=False, upload=text_file)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
