from django.db import models

# Create your models here.
class PresenceFile(models.Model):
    file_name = models.CharField(max_length=200)
    comments = models.CharField(max_length=200)
    upload_date = models.DateTimeField('date uploaded')
    processing_status = models.BooleanField()

    # The primary_key argument isn’t supported and will raise an error if used.
    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#filefield
    # file will be uploaded to MEDIA_ROOT/uploads/presence/
    upload = models.FileField(upload_to='uploads/presence/')
