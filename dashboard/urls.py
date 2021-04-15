from django.urls import path
from django.views.generic import TemplateView

from . import views

# Trigger registration of Dash Apps
from dashboard.dash_apps import simpleexample

urlpatterns = [
    path('', views.index, name='index'),
    path('presence/', views.presence, name='presence'),
    path('presence/upload', views.presence_upload, name='presence-upload'),
    path('presence/process/<int:id>', views.presence_process, name='presence-process'),
    path('simpleexample', TemplateView.as_view(template_name='dashboard/simpleexample.html'), name="demo-one"),
]
