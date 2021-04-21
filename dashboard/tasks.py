from celery import shared_task

from dashboard.models import PresenceFile, WeatherFile
from dashboard.processing.presence import process_presence_file

# celery -A AgrifoodIT worker -l info --pool=solo
from dashboard.processing.weather import process_weather_file


@shared_task()
def processNewPresenceFile(id):
    latest_unprocessed_files = PresenceFile.objects.filter(processing_status=False)
    print(f'Found {len(latest_unprocessed_files)} files to process')
    for file in latest_unprocessed_files:
        print('')
        print(f'===== {file.file_name} =====')
        process_presence_file(file.id)
        print(f'===== ====== =====')

    return f'Completed processing {len(latest_unprocessed_files)} files'

@shared_task()
def processNewWeatherFiles():
    latest_unprocessed_files = WeatherFile.objects.filter(processing_status=False)
    print(f'Found {len(latest_unprocessed_files)} files to process')
    for file in latest_unprocessed_files:
        print('')
        print(f'===== {file.file_name} =====')
        process_weather_file(file.id)
        print(f'===== ====== =====')

    return f'Completed processing {len(latest_unprocessed_files)} files'
