from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import PresenceFile, WeatherFile

# Create your views here.
from .processing.presence import process_presence_file
from .processing.weather import process_weather_file


def index(request):
    return render(request, 'dashboard/index.html')


def presence(request):
    latest_presence_files = PresenceFile.objects.order_by('-upload_date')[:50]
    context = {'latest_presence_files': latest_presence_files}
    return render(request, 'dashboard/presence.html', context)


def presence_upload(request):
    if request.method == 'POST':
        text_file = request.FILES.get('file')
        PresenceFile.objects.create(file_name=text_file.name, processing_status=False, upload=text_file)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def presence_process(request, id):
    return JsonResponse(process_presence_file(id))

def weather(request):
    latest_weather_files = WeatherFile.objects.order_by('-upload_date')[:50]
    context = {'latest_weather_files': latest_weather_files}
    return render(request, 'dashboard/weather.html', context)


def weather_upload(request):
    if request.method == 'POST':
        text_file = request.FILES.get('file')
        WeatherFile.objects.create(file_name=text_file.name, processing_status=False, upload=text_file)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def weather_process(request, id):
    return JsonResponse(process_weather_file(id))
