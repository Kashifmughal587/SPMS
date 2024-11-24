from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admindashboard'),
    path('students/', views.student_list, name="studentlist"),
    path('addstudent/', views.add_student, name="addstudent"),
    path('studentdetail/<int:student_id>/', views.student_detail, name="studentdetail")
]
