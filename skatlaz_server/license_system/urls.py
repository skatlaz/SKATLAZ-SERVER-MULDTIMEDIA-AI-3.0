from django.urls import path
from . import views

urlpatterns = [
    path('activate/', views.activate, name='license_activate'),
    path('status/', views.status, name='license_status'),
]
