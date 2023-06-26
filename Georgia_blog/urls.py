"""
URL configuration for Georgia_blog project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from Georgia_blog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)