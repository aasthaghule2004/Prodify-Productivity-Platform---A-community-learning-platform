from django.contrib import admin

from .models import FocusSession


@admin.register(FocusSession)
class FocusSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "task_name", "planned_minutes", "elapsed_seconds", "completed", "started_at", "ended_at")
    list_filter = ("completed", "started_at", "ended_at")
    search_fields = ("user__username", "task_name")
    ordering = ("-started_at",)
