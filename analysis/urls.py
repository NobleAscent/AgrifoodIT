from django.urls import path
from django.views.generic import TemplateView

from . import views

# Trigger registration of Dash Apps
from analysis.dash_apps import simpleexample

urlpatterns = [
    path('dailyanalysis', TemplateView.as_view(template_name='analysis/dailyanalysis.html'), name="daily-analysis"),
    path('rohit', views.simpleFPmining, name="rohit-analysis"),
]
