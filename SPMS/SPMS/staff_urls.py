from django.urls import path
from .views import staff_views

urlpatterns = [
    path('dashboard/', staff_views.dashboard, name='staff_dashboard'),
]
