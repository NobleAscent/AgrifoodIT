from django.contrib import admin
from .models import PresenceFile, Pig, Presence

admin.site.register(PresenceFile)
admin.site.register(Pig)
admin.site.register(Presence)