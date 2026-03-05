from django.contrib import admin

from .models import Folder, StudyMaterial


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "user__username")
    ordering = ("-created_at",)


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "folder", "is_pinned", "uploaded_at")
    list_filter = ("is_pinned", "uploaded_at")
    search_fields = ("title", "folder__name", "folder__user__username")
    ordering = ("-uploaded_at",)
