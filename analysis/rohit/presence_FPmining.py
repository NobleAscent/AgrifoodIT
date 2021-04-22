import datetime

import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder

from dashboard.models import Weather, Presence


def FPGrowth(dataset, min_support, min_length, min_support_of_custom_itemsets):
    frequent_itemsets = fpgrowth(df=dataset, min_support=min_support,
                                 use_colnames=True, max_len=None)

    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))

    freq_items = frequent_itemsets[(frequent_itemsets['length'] >= min_length) &
                                   (frequent_itemsets['support'] >= min_support_of_custom_itemsets)]
    return freq_items

def generate_dataframe_for_FPGrowth(primary_key):
    te = TransactionEncoder()

    entryExitPairs : list = summarizedEntryExit(primary_key=primary_key)
    range_dataset = []

    for pair in entryExitPairs:
        range_dataset.append(discretize_range_values_data(pair[2].temperature, pair[2].pressure, pair[2].humidity))

    print('Printing Range Dataset')
    print(range_dataset)

    te_ary = te.fit(range_dataset).transform(range_dataset)
    return pd.DataFrame(te_ary, columns=te.columns_)


# + Pig 20 2020-07-16 07:04:53.767000 temperature: 17.36°C pressure: 1103.83hPa humidity: 54.84%
# - Pig 20 2020-07-16 07:04:58.768000 temperature: 17.36°C pressure: 1103.83hPa humidity: 54.84%
def summarizedEntryExit(primary_key) -> list:
    dataset = []
    processed_until_timestamp: datetime = datetime.datetime(2000, 1, 1)
    for _presence in Presence.objects.filter(direction=True,
                                             pig_rfid=primary_key):

        if processed_until_timestamp > _presence.timestamp:
            continue

        # Create time range of 30 minutes
        start_of_30_minutes = _presence.timestamp
        end_of_30_minutes = start_of_30_minutes + datetime.timedelta(minutes=30)
        processed_until_timestamp = end_of_30_minutes

        exit_of_pig = Presence.objects.filter(timestamp__range=(start_of_30_minutes, end_of_30_minutes),
                                              direction=False, pig_rfid=_presence.pig_rfid).order_by(
            'timestamp')

        furthest_exit_of_pig = exit_of_pig.last()

        closest_weather = Weather.objects.filter(timestamp__range=(start_of_30_minutes, end_of_30_minutes)).first()

        # To get average we would have to query the database further so it's better to take closest now
        # average_weather = Weather.objects.filter(timestamp__range=(start_of_30_minutes, end_of_30_minutes))
        # average_temperature = round(average_weather.aggregate(Avg('temperature'))['temperature__avg'], 2)
        # average_pressure = round(average_weather.aggregate(Avg('pressure'))['pressure__avg'], 2)
        # average_humidity = round(average_weather.aggregate(Avg('humidity'))['humidity__avg'], 2)

        # TODO: Temporary fix incase we don't find weather
        if not closest_weather:
            continue

        print(
            f'{"+" if _presence.direction else "-"} '
            f'{_presence.pig_rfid.nickname} '
            f'{_presence.timestamp} '
            f'temperature: {closest_weather.temperature}°C '
            f'pressure: {closest_weather.pressure}hPa '
            f'humidity: {closest_weather.humidity}%')
        print(
            f'{"+" if furthest_exit_of_pig.direction else "-"} '
            f'{furthest_exit_of_pig.pig_rfid.nickname} '
            f'{furthest_exit_of_pig.timestamp} '
            f'temperature: {closest_weather.temperature}°C '
            f'pressure: {closest_weather.pressure}hPa '
            f'humidity: {closest_weather.humidity}%')

        dataset.append([_presence, furthest_exit_of_pig, closest_weather])

    return dataset

def discretize_range_values_data(temp: float, pressure: float, humidity: float) -> list:
    if 0 > temp >= -10:
        temp = '0to-10-temp'
    elif -10 > temp >= -20:
        temp = '-10to-20-temp'
    elif 0 <= temp < 10:
        temp = '0to+10-temp'
    elif 10 <= temp < 20:
        temp = '+10to+20-temp'
    elif 20 <= temp < 30:
        temp = '+20to+30-temp'
    elif 30 <= temp < 40:
        temp = '+30to+40-temp'
    else:
        temp = 'other-temp'

    if 1100 > pressure >= 1080:
        pressure = '1080-1100-pressure'
    elif 1080 > pressure >= 1060:
        pressure = '1080-1060-pressure'
    elif 1100 <= pressure < 1120:
        pressure = '1100-1120-pressure'
    elif 1120 <= pressure < 1140:
        pressure = '1120-1140-pressure'
    else:
        pressure = 'other-pressure'

    if humidity < 25:
        humidity = '0-25-hum'
    elif 25 <= humidity < 50:
        humidity = '25-50-hum'
    elif 50 <= humidity < 75:
        humidity = '50-75-hum'
    elif 75 <= humidity <= 100:
        humidity = '75-100-hum'

    return [temp, pressure, humidity]
