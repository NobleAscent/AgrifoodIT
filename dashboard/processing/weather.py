from datetime import datetime

from dashboard.models import PresenceFile, Weather, WeatherFile


def process_weather_file(primary_key) -> dict:
    response_dict = {'Total lines': 0, 'Processed lines': 0}
    try:
        weather_file = PresenceFile.objects.get(pk=primary_key)
        weather_file.upload.open(mode='r')

        line_list: list = weather_file.upload.readlines()
        response_dict['Total lines'] = len(line_list)

        # Remove all previous existing processed lines if any
        Weather.objects.filter(weather_file=primary_key).delete()

        # Read each line in the text file
        for line in line_list:
            process_weather_line(line, weather_file)
            response_dict['Processed lines'] += 1

        # Update the File row to indicate that this file has been processed.
        weather_file.comments = \
            f'Processed lines:{response_dict["Processed lines"]} Errors:{response_dict["Total lines"] - response_dict["Processed lines"]}'
        weather_file.processing_status = True
        weather_file.save()
    except ValueError as exception:
        return response_dict
    else:
        return response_dict


def process_weather_line(line: str, file: WeatherFile) -> Weather:
    try:
        line_dict = validate_weather_line(line)

        # All error test cases passed so lets create new entry in Presence table
        row = Weather()
        row.weather_file = file
        row.temperature = line_dict['temperature']
        row.pressure = line_dict['pressure']
        row.humidity = line_dict['humidity']
        row.timestamp = line_dict['date']
        row.save()

        return row
    except ValueError as exception:
        return False


def validate_weather_line(line: str) -> dict:
    # Example of a sample line in a weather.txt file
    # temperature: -1.34°C, pressure: 1114.18hPa, humidity:  92.09%, time: 2021-02-20T00:00:31.451 \n
    if len(line) == 0:
        raise ValueError('Empty Input')

    # We have to check if line is too short or contains more elements than we need.
    line_split = line.strip().split(',')
    if len(line_split) != 4:
        raise ValueError('Input does not split into 4 parts')

    # Populate the dictionary
    # The dictionary makes it easier to change the format later on.
    # It also makes the code more readable as compared to using indexes
    line_dict = {'temperature': line_split[0].strip()[12:-2].strip(),
                 'pressure': line_split[1].strip()[9:-3].strip(),
                 'humidity': line_split[2].strip()[10:-1].strip(),
                 'date': line_split[3].strip()[5:].strip()}

    try:
        line_dict['temperature'] = float(line_dict['temperature'])
        if line_dict['temperature'] <= -50.00 or line_dict['temperature'] >= 50.00:
            raise ValueError('Out of Range Temperature. Limit is 50.00°C to -50.00°C')
    except ValueError as exception:
        raise ValueError('Out of Range Temperature. Limit is 50.00°C to -50.00°C')

    try:
        line_dict['pressure'] = float(line_dict['pressure'])
        if line_dict['pressure'] <= 1000.00 or line_dict['pressure'] >= 1500.00:
            raise ValueError('Out of Range Pressure. Limit is 1000.00hPa to 1500.00hPa')
    except ValueError as exception:
        raise ValueError('Out of Range Pressure. Limit is 1000.00hPa to 1500.00hPa')

    try:
        line_dict['humidity'] = float(line_dict['humidity'])
        if line_dict['humidity'] <= 0.00 or line_dict['humidity'] > 100.00:
            raise ValueError('Out of Range Humidity. Limit is 0.00% to 100.00%')
    except ValueError as exception:
        raise ValueError('Out of Range Humidity. Limit is 0.00% to 100.00%')

    # Check if date can be correctly parsed by built in method
    # If date is incorrect fromisoformat() will throw ValueError
    try:
        line_dict['date'] = datetime.fromisoformat(line_dict['date'])
    except ValueError as exception:
        raise ValueError('Invalid DateTime')

    return line_dict
