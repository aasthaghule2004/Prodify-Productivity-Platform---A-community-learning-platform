from django.urls import path
from . import views

urlpatterns = [
    path('', views.timer_view, name='timer'),
    path('session/start/', views.start_session, name='start_session'),
    path('session/update/', views.update_session, name='update_session'),
]
