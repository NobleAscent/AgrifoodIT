from django.db import models

# Create your models here.
class PresenceFile(models.Model):
    file_name = models.CharField(max_length=200)
    upload_date = models.DateTimeField('date uploaded')
    processing_status = models.BooleanField()
    comments = models.CharField(max_length=200)
