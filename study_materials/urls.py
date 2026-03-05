from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.folders_list, name="folders"),
    path("folder/<int:folder_id>/", views.folder_detail, name="folder_detail"),
    path("delete/<int:material_id>/", views.delete_material, name="delete_material"),
    path("toggle-pin/<int:material_id>/", views.toggle_pin, name="toggle_pin"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)