from dashboard.models import Weather, Presence, Pig
import datetime
from collections import defaultdict

# Output:
# + 4 Pig 14 2020-07-16 03:03:42.116000 temperature: 11.7°C pressure: 1103.14hPa humidity: 11.7%
# - 4 Pig 14 2020-07-16 03:03:47.118000 temperature: 11.7°C pressure: 1103.14hPa humidity: 11.7%
# + 3 Pig 13 2020-07-16 04:07:48.304000 temperature: 12.59°C pressure: 1103.07hPa humidity: 12.59%
# - 3 Pig 13 2020-07-16 04:07:53.305000 temperature: 12.59°C pressure: 1103.07hPa humidity: 12.59%
# + 4 Pig 19 2020-07-16 04:12:56.329000 temperature: 12.61°C pressure: 1103.04hPa humidity: 12.61%
# + 3 Pig 19 2020-07-16 04:12:58.633000 temperature: 12.61°C pressure: 1103.04hPa humidity: 12.61%
def mergePresenceWithWeather():
    for _presence in Presence.objects.filter(timestamp__date=datetime.date(2020, 7, 16)):
        previous_minute = _presence.timestamp - datetime.timedelta(minutes=1)
        previous_minute = previous_minute.replace(second=0, microsecond=0)
        next_minute = previous_minute + datetime.timedelta(minutes=1)

        closest_weather = Weather.objects.filter(timestamp__range=(previous_minute, next_minute)).first()

        print(
            f'{"+" if _presence.direction else "-"} '
            f'{_presence.reader} '
            f'{_presence.pig_rfid.nickname} '
            f'{_presence.timestamp} '
            f'temperature: {closest_weather.temperature}°C '
            f'pressure: {closest_weather.pressure}hPa '
            f'humidity: {closest_weather.temperature}%')

# Output:
# Pig 12 => Entry at 2020-07-16 19:32:48.087000 Exit at 2020-07-16 19:32:53.125000 Time Elapsed 5.038
# Pig 8 => Entry at 2020-07-16 19:32:51.124000 Exit at 2020-07-16 19:33:11.335000 Time Elapsed 20.211
# Pig 8 => Entry at 2020-07-16 19:33:09.334000 Exit at 2020-07-16 19:33:11.335000 Time Elapsed 2.001
# Pig 8 => Entry at 2020-07-16 19:33:27.641000 Exit at 2020-07-16 19:33:32.642000 Time Elapsed 5.001
# Pig 8 => Entry at 2020-07-16 19:33:41.663000 Exit at 2020-07-16 19:33:48.086000 Time Elapsed 6.423
# Pig 11 => Entry at 2020-07-16 19:42:04.172000 Exit at 2020-07-16 19:42:09.173000 Time Elapsed 5.001
# Pig 16 => Entry at 2020-07-16 20:21:56.953000 Exit at 2020-07-16 20:22:01.955000 Time Elapsed 5.002
def findPigEntryExit():
    for _presence in Presence.objects.filter(timestamp__date=datetime.date(2020, 7, 16)):

        # If the pig exits the area then skip processing
        if not _presence.direction:
            continue

        # Pig has entered the area. Lets find when it exits and after how long
        _presence_exit = Presence.objects.filter(timestamp__date=datetime.date(2020, 7, 16),
                                                 pig_rfid=_presence.pig_rfid,
                                                 direction=False,
                                                 timestamp__gte=_presence.timestamp).first()

        print(
            f'{_presence.pig_rfid.nickname} => '
            f'Entry at {_presence.timestamp} '
            f'Exit at {_presence_exit.timestamp} '
            f'Time Elapsed {(_presence_exit.timestamp - _presence.timestamp).total_seconds()}')


# Output: defaultdict(<class 'int'>, {'Pig 14': 16, 'Pig 13': 12, 'Pig 19': 29, 'Pig 15': 6, 'Pig 6': 2, 'Pig 7': 3,
# 'Pig 11': 7, 'Pig 3': 3, 'Pig 8': 10, 'Pig 16': 36, 'Pig 18': 2, 'Pig 20': 1, 'Pig 17': 7, 'Pig 10': 5,
# 'Pig 5': 15, 'Pig 12': 1})
def total_count_of_occurrences():
    count_dictionary = defaultdict(int)
    for _presence in Presence.objects.filter(timestamp__date=datetime.date(2020, 7, 16)):

        # If the pig exits the area then skip processing
        if not _presence.direction:
            continue

        # Pig has entered the area. Lets find when it exits and after how long
        _presence_exit = Presence.objects.filter(timestamp__date=datetime.date(2020, 7, 16),
                                                 pig_rfid=_presence.pig_rfid,
                                                 direction=False,
                                                 timestamp__gte=_presence.timestamp).first()

        count_dictionary[_presence.pig_rfid.nickname] += 1

    print(count_dictionary)
