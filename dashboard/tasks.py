from celery import shared_task

from dashboard.models import PresenceFile
from dashboard.processing.presence import process_presence_file

# celery -A AgrifoodIT worker -l info --pool=solo

@shared_task()
def processNewFiles():
    latest_unprocessed_files = PresenceFile.objects.filter(processing_status=False)
    print(f'Found {len(latest_unprocessed_files)} files to process')
    for file in latest_unprocessed_files:
        print('')
        print(f'===== {file.file_name} =====')
        process_presence_file(file.id)
        print(f'===== ====== =====')

    return f'Completed processing {len(latest_unprocessed_files)} files'
