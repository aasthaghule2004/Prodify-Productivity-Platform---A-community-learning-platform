from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),

   
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', RedirectView.as_view(pattern_name='profile', permanent=False)),

    path('', include('accounts.urls')),
    path('todo/', include('todo.urls')),
    path('timer/', include('timer.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('study_materials/', include('study_materials.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Demo deployment media serving. For production, use persistent object storage.
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
