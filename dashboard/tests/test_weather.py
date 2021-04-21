from datetime import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from dashboard.models import WeatherFile
from dashboard.processing.weather import process_weather_line, validate_weather_line


class WeatherFileProcessingTestCase(TestCase):
    def setUp(self):
        sample_file = WeatherFile(file_name='20210220_weather.txt')
        sample_file.processing_status = False

        # How to unittest a FileField because I don't want to save the
        # file on disk. It is better to have it in code.
        # https://stackoverflow.com/questions/4283933/what-is-the-clean-way-to-unittest-filefield-in-django
        # Use triple quotes to create a multiline string
        # note the b in front of the string [bytes]
        sample_file.upload = SimpleUploadedFile(
            '20210220_weather.txt',
            bytes("""temperature: -1.34°C, pressure: 1114.18hPa, humidity:  92.09%, time: 2021-02-20T00:00:31.451 
                temperature: -1.40°C, pressure: 1114.13hPa, humidity:  92.06%, time: 2021-02-20T00:01:31.481 
                temperature: -1.40°C, pressure: 1114.19hPa, humidity:  92.04%, time: 2021-02-20T00:02:31.511 
                temperature: -1.42°C, pressure: 1114.22hPa, humidity:  92.03%, time: 2021-02-20T00:03:31.541 
                temperature: -1.44°C, pressure: 1114.28hPa, humidity:  92.02%, time: 2021-02-20T00:04:31.571 
                temperature: -1.57°C, pressure: 1114.07hPa, humidity:  92.02%, time: 2021-02-20T00:05:31.601 
                temperature: -1.42°C, pressure: 1114.35hPa, humidity:  92.07%, time: 2021-02-20T00:06:31.631 
                temperature: -1.39°C, pressure: 1114.35hPa, humidity:  92.13%, time: 2021-02-20T00:07:31.661 
                temperature: -1.33°C, pressure: 1114.31hPa, humidity:  92.20%, time: 2021-02-20T00:08:31.691 
                temperature: -1.29°C, pressure: 1114.39hPa, humidity:  92.26%, time: 2021-02-20T00:09:31.721 
                temperature: -1.25°C, pressure: 1114.34hPa, humidity:  92.33%, time: 2021-02-20T00:10:31.750 
                temperature: -1.20°C, pressure: 1114.22hPa, humidity:  92.39%, time: 2021-02-20T00:11:31.780 
                temperature: -1.18°C, pressure: 1114.24hPa, humidity:  92.47%, time: 2021-02-20T00:12:31.810 
                temperature: -1.14°C, pressure: 1114.24hPa, humidity:  92.57%, time: 2021-02-20T00:13:31.840 
                temperature: -1.14°C, pressure: 1114.28hPa, humidity:  92.70%, time: 2021-02-20T00:14:31.870 
                temperature: -1.12°C, pressure: 1114.25hPa, humidity:  92.80%, time: 2021-02-20T00:15:31.900 
                temperature: -1.09°C, pressure: 1114.22hPa, humidity:  92.97%, time: 2021-02-20T00:16:31.930 
                temperature: -1.05°C, pressure: 1114.23hPa, humidity:  93.10%, time: 2021-02-20T00:17:31.960 
                temperature: -1.03°C, pressure: 1114.30hPa, humidity:  93.21%, time: 2021-02-20T00:18:31.990 
                temperature: -1.03°C, pressure: 1114.24hPa, humidity:  93.28%, time: 2021-02-20T00:19:32.020 
                temperature: -1.02°C, pressure: 1114.19hPa, humidity:  93.36%, time: 2021-02-20T00:20:32.050"""
                  , 'utf-8'))
        sample_file.save()

    # Test case to check if string parsing is working correctly and
    # we are getting a proper PresenceLine object from a string
    def test_process_valid_line(self):
        # Correct Input
        row = process_weather_line(
            'temperature: -1.34°C, pressure: 1114.18hPa, humidity:  92.09%, time: 2021-02-20T00:00:31.451',
            WeatherFile.objects.first())
        self.assertEqual(-1.34, row.temperature)
        self.assertEqual(1114.18, row.pressure)
        self.assertEqual(92.09, row.humidity)
        self.assertEqual(datetime.fromisoformat('2021-02-20T00:00:31.451'), row.timestamp)

    # Test case to check erroneous data input causes exception to be thrown
    # https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception/129610#129610
    def test_process_invalid_line(self):
        self.assertRaisesRegex(ValueError, 'Empty Input', validate_weather_line, '')

        self.assertRaisesRegex(ValueError, r'^Out of Range Temperature. Limit is 50.00°C to -50.00°C$',
                               validate_weather_line,
                               'temperature: -1000.34°C, pressure: 1114.18hPa, humidity:  92.09%, time: 2021-02-20T00:00:31.451')

        self.assertRaisesRegex(ValueError, r'^Out of Range Pressure. Limit is 1000.00hPa to 1500.00hPa$',
                               validate_weather_line,
                               'temperature: -1.34°C, pressure: 5000.18hPa, humidity:  92.09%, time: 2021-02-20T00:00:31.451')

        self.assertRaisesRegex(ValueError, r'^Out of Range Humidity. Limit is 0.00% to 100.00%$', validate_weather_line,
                               'temperature: -1.34°C, pressure: 1114.18hPa, humidity:  101.00%, time: 2021-02-20T00:00:31.451')

        self.assertRaisesRegex(ValueError, r'^Invalid DateTime$', validate_weather_line,
                               'temperature: -1.34°C, pressure: 1114.18hPa, humidity:  92.09%, time: ABCD-07-13W19:39T:05.998')

        self.assertRaisesRegex(ValueError, r'^Input does not split into 4 parts$', validate_weather_line,
                               'temperature: -1.34°C, pressure: 1114.18hPa, humidity:  92.09%, time: 2021-02-20T00:00:31.451, #, 4, E20000195206006314302257')
