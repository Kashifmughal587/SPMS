from django.urls import path
from .views import admin_views

urlpatterns = [
    path('dashboard/', admin_views.dashboard, name='admin_dashboard'),
]
