# Create your tasks here
from datetime import datetime

from celery import shared_task
from django.db.models import Q

from .models import PresenceFile, Presence, Pig


@shared_task
def process_presence_file(primary_key):
    presence_file = PresenceFile.objects.get(pk=primary_key)
    presence_file.upload.open(mode='r')

    # Read each line in the text file
    for line in presence_file.upload.readlines():
        # - 4 E200001999130097264042CC 2020-07-17T19:33:03.669 \n
        # ('-','4','E200001999130097264042CC','2020-07-17T19:33:03.669')
        line_array = line.strip().split(' ')

        # I don't want to use regex to validate as it will become complex or long
        empty = False
        comment = ''
        for i in range(len(line_array)):
            if line_array[i] == '':
                empty = True

        # There was some missing data e.g RFID is missing
        if empty:
            comment += f'Skipping Empty Input {str(line_array)} \n'

        # Could not find Pig with that RFID
        pig_fk = Pig.objects.get(pk=line_array[2])
        # if !pig_fk.exists():
        #     comment += f'Skipping Unknown RFID {str(line_array)} \n'

        print(comment)
        new_presence = Presence(pig_rfid=pig_fk,
                                direction=(line_array[0] == '+'),
                                reader=(line_array[1]),
                                timestamp=line_array[3])
        new_presence.save()

        presence_file.comments = comment
        presence_file.processing_status = True
        presence_file.save()

# Returns Presence model object
def process_presence_line(line):
    # Example of a sample line in a presence.txt file
    # - 4 E200001999130097264042CC 2020-07-17T19:33:03.669 \n
    line_array = line.strip().split(' ')
    row = Presence()
    row.direction = line_array[0] == '+'
    row.reader = int(line_array[1])

    # https://stackoverflow.com/questions/45253994/django-filter-with-or-statement
    row.pig_rfid = Pig.objects.get(Q(rfid_A=line_array[2]) | Q(rfid_B=line_array[2]))
    row.timestamp = datetime.fromisoformat(line_array[3])
    return row
