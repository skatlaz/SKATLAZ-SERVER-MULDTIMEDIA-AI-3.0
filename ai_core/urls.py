from django.urls import path
from . import views

app_name = 'ai_core'
urlpatterns = [
    path('', views.client_home, name='client_home'),
    path('client/', views.client_home, name='client_home_alias'),
    path('config/', views.mcp_config, name='mcp_config'),
    path('registry/', views.mcp_registry, name='mcp_registry'),
    path('pipelines/', views.pipelines, name='pipelines'),
    path('mcp-task/', views.mcp_task, name='mcp_task'),
]
