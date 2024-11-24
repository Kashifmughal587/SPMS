from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='adminDashboard'),
    path('students/', views.student_list, name="studentList"),
    path('studentdetail/<int:student_id>/', views.student_detail, name="studentDetail")
]
