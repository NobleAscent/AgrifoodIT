from django.contrib import admin
from .models import PresenceFile, Pig, Presence, WeatherFile, Weather

admin.site.register(Pig)
admin.site.register(PresenceFile)
admin.site.register(Presence)

admin.site.register(WeatherFile)
admin.site.register(Weather)