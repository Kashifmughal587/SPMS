from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.login, name = 'login'),
    path('login_process/', views.login_process, name = 'login_process'),
    path('logout/', views.logout, name = 'logout'),
    path('admin/', admin.site.urls),
    path('administration/', include('SPMS.admin_urls')),
    path('staff/', include('SPMS.staff_urls')),
    path('student/', include('SPMS.student_urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
