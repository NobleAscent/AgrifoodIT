from celery import shared_task

from dashboard.models import PresenceFile, WeatherFile
from dashboard.processing.presence import process_presence_file

# celery -A AgrifoodIT worker -l info --pool=solo
from dashboard.processing.weather import process_weather_file


@shared_task()
def processNewPresenceFile(primary_key):
    file = PresenceFile.objects.get(pk=primary_key)
    print(f'===== {file.file_name} ===== START')
    process_presence_file(file.id)
    print(f'===== {file.file_name} ===== DONE')
    return {"status": True}

@shared_task()
def processNewWeatherFile(primary_key):
    file = WeatherFile.objects.get(pk=primary_key)
    print(f'===== {file.file_name} ===== START')
    process_weather_file(file.id)
    print(f'===== {file.file_name} ===== DONE')
    return {"status": True}
