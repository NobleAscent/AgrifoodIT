from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('presence/', views.presence, name='presence'),
    path('presence/upload', views.presence_upload, name='presence-upload'),
    path('presence/process/<int:id>', views.presence_process, name='presence-process')
]
