import re
from datetime import datetime

from django.db.models import Q

from dashboard.models import PresenceFile, Presence, Pig
from django.core.exceptions import ObjectDoesNotExist

def process_presence_line(line: str, file: PresenceFile) -> Presence:
    try:
        line_dict = validate_presence_line(line)

        # All error test cases passed so lets create new entry in Presence table
        row = Presence()
        row.presence_file = file
        row.direction = line_dict['direction']
        row.reader = int(line_dict['sensor_number'])

        # https://stackoverflow.com/questions/45253994/django-filter-with-or-statement
        row.pig_rfid = Pig.objects.get(Q(rfid_A=line_dict['RFID']) | Q(rfid_B=line_dict['RFID']))
        row.timestamp = line_dict['date']
        row.save()

        return row
    except ValueError as exception:
        return False


def process_presence_file(primary_key) -> dict:
    response_dict = {'Total lines': 0, 'Processed lines': 0}
    try:
        presence_file = PresenceFile.objects.get(pk=primary_key)
        presence_file.upload.open(mode='r')

        line_list: list = presence_file.upload.readlines()
        response_dict['Total lines'] = len(line_list)

        # Remove all previous existing processed lines if any
        Presence.objects.filter(presence_file=primary_key).delete()

        # Read each line in the text file
        for line in line_list:
            process_presence_line(line, presence_file)
            response_dict['Processed lines'] += 1

        # Update the File row to indicate that this file has been processed.
        presence_file.comments = \
            f'Processed lines:{response_dict["Processed lines"]} Errors:{response_dict["Total lines"] - response_dict["Processed lines"]}'
        presence_file.processing_status = True
        presence_file.save()
    except ValueError as exception:
        return response_dict
    else:
        return response_dict


# https://medium.com/@ageitgey/learn-how-to-use-static-type-checking-in-python-3-6-in-10-minutes-12c86d72677b
# Returns Presence model object
def validate_presence_line(line: str) -> dict:
    # Example of a sample line in a presence.txt file
    # - 4 E200001999130097264042CC 2020-07-17T19:33:03.669 \n
    if len(line) == 0:
        raise ValueError('Empty Input')

    # We have to check if line is too short or contains more elements than we need.
    line_split = line.strip().split(' ')
    if len(line_split) != 4:
        raise ValueError('Input does not split into 4 parts')

    # Populate the dictionary
    # The dictionary makes it easier to change the format later on.
    # It also makes the code more readable as compared to using indexes
    line_dict = {'direction': line_split[0], 'sensor_number': line_split[1], 'RFID': line_split[2],
                 'date': line_split[3]}

    # Regex Patterns with Named Capturing Groups
    direction_pattern = re.compile(r'\+|\-')
    # sensor_number_pattern = re.compile(r'\d')
    rfid_pattern = re.compile(r'[0-9A-Z]{24}')

    # Regex Error Checking
    if not direction_pattern.match(line_dict['direction']):
        raise ValueError('Expected + or - for direction')
    line_dict['direction'] = line_dict['direction'] == '+'

    try:
        line_dict['sensor_number'] = int(line_dict['sensor_number'])
    except ValueError as exception:
        raise ValueError('Incorrect reader number format')
    if not 0 < line_dict['sensor_number'] < 10:
        raise ValueError('Incorrect reader number format')
    if not rfid_pattern.match(line_dict['RFID']):
        raise ValueError('Incorrect RFID format')

    # Check if date can be correctly parsed by built in method
    # If date is incorrect fromisoformat() will throw ValueError
    try:
        line_dict['date'] = datetime.fromisoformat(line_dict['date'])
    except ValueError as exception:
        raise ValueError('Invalid DateTime')

    if not rfid_exists(line_dict['RFID']):
        raise ValueError('RFID does not exist')

    return line_dict


def rfid_exists(rfid: str) -> bool:
    try:
        Pig.objects.get(Q(rfid_A=rfid) | Q(rfid_B=rfid))

    # https://stackoverflow.com/questions/52455835/where-do-i-import-the-doesnotexist-exception-in-django-1-10-from
    except ObjectDoesNotExist as exception:
        return False
    else:
        return True