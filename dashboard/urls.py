from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('metrics/', views.dashboard_metrics, name='dashboard_metrics'),
]
