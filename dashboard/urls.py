from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),

    path('presence/', views.presence, name='presence'),
    path('presence/upload', views.presence_upload, name='presence-upload'),
    path('presence/process/<int:id>', views.presence_process, name='presence-process'),

    path('weather/', views.weather, name='weather'),
    path('weather/upload', views.weather_upload, name='weather-upload'),
    path('weather/process/<int:id>', views.weather_process, name='weather-process'),

    path('dailyanalysis', TemplateView.as_view(template_name='dashboard/../analysis/templates/analysis/dailyanalysis.html'), name="daily-analysis"),
]
