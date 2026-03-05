from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "completed", "created_at", "completed_at")
    list_filter = ("completed", "created_at", "completed_at")
    search_fields = ("user__username", "title")
    ordering = ("-created_at",)
