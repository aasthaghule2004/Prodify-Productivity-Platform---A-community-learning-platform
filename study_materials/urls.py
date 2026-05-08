from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", views.folders_list, name="folders"),
    re_path(r"^folder/+$", RedirectView.as_view(pattern_name="folders", permanent=False)),
    path("folder/<int:folder_id>/", views.folder_detail, name="folder_detail"),
    path("delete/<int:material_id>/", views.delete_material, name="delete_material"),
    path("toggle-pin/<int:material_id>/", views.toggle_pin, name="toggle_pin"),
]
