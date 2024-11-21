from django.urls import path
from .views import student_views

urlpatterns = [
    path('dashboard/', student_views.dashboard, name='student_dashboard'),
]
