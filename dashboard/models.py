from datetime import datetime
from django.db import models

# Create your models here.
class PresenceFile(models.Model):
    file_name = models.CharField(max_length=200)
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
    rfid = models.CharField(primary_key=True, max_length=200)
    nickname = models.CharField(max_length=50)

    def __str__(self):
        return self.nickname

class Presence(models.Model):
    # many-to-one (many Presence for one Pig)
    pig_rfid = models.ForeignKey(Pig, on_delete=models.CASCADE)

    direction = models.BooleanField()
    reader = models.IntegerField()
    timestamp = models.DateTimeField()
