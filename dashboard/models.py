from django.db import models


# Create your models here.
class PresenceFile(models.Model):
    file_name = models.CharField(max_length=200, unique=True)
    comments = models.CharField(max_length=200)

    # using auto_now_add renders the field un-editable in the admin
    upload_date = models.DateTimeField('date uploaded', auto_now_add=True)
    processing_status = models.BooleanField()

    # The primary_key argument isn’t supported and will raise an error if used.
    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#filefield
    # file will be uploaded to MEDIA_ROOT/uploads/presence/
    upload = models.FileField(upload_to='uploads/presence/')

    def __str__(self):
        return self.file_name


# This model can be populated by seeding the database
# https://docs.djangoproject.com/en/3.1/topics/migrations/#data-migrations
class Pig(models.Model):
    rfid_A = models.CharField(max_length=200, unique=True)
    rfid_B = models.CharField(max_length=200, unique=True)
    weight = models.IntegerField(default=-1)
    nickname = models.CharField(max_length=50)

    def __str__(self):
        return self.nickname


class Presence(models.Model):
    # Example of a sample line in a presence.txt file
    # - 4 E200001999130097264042CC 2020-07-17T19:33:03.669 \n
    # True is +
    # False is -
    direction = models.BooleanField()
    reader = models.IntegerField()

    # many-to-one (many Presence for one Pig)
    pig_rfid = models.ForeignKey(Pig, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    presence_file = models.ForeignKey(PresenceFile, on_delete=models.CASCADE)

# Create your models here.
class WeatherFile(models.Model):
    file_name = models.CharField(max_length=200, unique=True)
    comments = models.CharField(max_length=200)

    # using auto_now_add renders the field un-editable in the admin
    upload_date = models.DateTimeField('date uploaded', auto_now_add=True)
    processing_status = models.BooleanField()

    # The primary_key argument isn’t supported and will raise an error if used.
    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#filefield
    # file will be uploaded to MEDIA_ROOT/uploads/weather/
    upload = models.FileField(upload_to='uploads/weather/')

    def __str__(self):
        return self.file_name

class Weather(models.Model):
    # Example of a sample line in a presence.txt file
    # temperature: -9.38°C, pressure: 1115.44hPa, humidity:  59.55%, time: 2021-02-12T00:00:29.285 \n
    temperature = models.FloatField()
    pressure = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField()
    weather_file = models.ForeignKey(WeatherFile, on_delete=models.CASCADE)
