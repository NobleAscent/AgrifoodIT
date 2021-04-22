from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render
from datetime import date

from .models import PresenceFile, WeatherFile, Presence, Weather
from .processing.presence import process_presence_file
from .processing.weather import process_weather_file
from .tasks import processNewPresenceFile, processNewWeatherFile


def index(request):
    max_presence : date = Presence.objects.aggregate(Max('timestamp'))['timestamp__max'].date()
    max_weather : date = Weather.objects.aggregate(Max('timestamp'))['timestamp__max'].date()
    context = {'last_presence_upload': (date.today() - max_presence).days,
               'last_weather_upload': (date.today() - max_weather).days}
    return render(request, 'dashboard/index.html', context)


def presence(request):
    latest_presence_files = PresenceFile.objects.order_by('-upload_date')[:50]
    context = {'latest_presence_files': latest_presence_files}
    return render(request, 'dashboard/presence.html', context)


def presence_upload(request):
    if request.method == 'POST':
        text_file = request.FILES.get('file')
        file = PresenceFile.objects.create(file_name=text_file.name, processing_status=False, upload=text_file)
        processNewPresenceFile.delay(file.id)
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
        file = WeatherFile.objects.create(file_name=text_file.name, processing_status=False, upload=text_file)
        processNewWeatherFile.delay(file.id)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def weather_process(request, id):
    return JsonResponse(process_weather_file(id))
