from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo'),
    path('complete/<int:task_id>/', views.complete_task, name='complete'),
    path('delete/<int:task_id>/', views.delete_task, name='delete'),
]