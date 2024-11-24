from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('home.urls')),
    path('administrator/', include('administrator.urls')),
    path('teachers/', include('teachers.urls')),
    path('students/', include('students.urls')),
    path('parents/', include('parents.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)