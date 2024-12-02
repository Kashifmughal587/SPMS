from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admindashboard'),
    
    path('students/', views.student_list, name="studentlist"),
    path('studentsbyclass/', views.student_list_by_class, name="studentlistbyclass"),
    path('addstudent/', views.add_student, name="addstudent"),
    path('studentdetail/<int:student_id>/', views.student_detail, name="studentdetail"),
    
    # path('school_sessions/', views.school_session_list, name='school_session_list'),
    # path('add_school_session/', views.add_school_session, name='add_school_session'),
    # path('update_school_session/<int:session_id>/', views.update_school_session, name='update_school_session'),
    # path('delete_school_session/<int:session_id>/', views.delete_school_session, name='delete_school_session'),

    path('classes/', views.class_list, name='class_list'),
    path('add_class/', views.add_class, name='add_class'),
    path('update_class/<int:class_id>/', views.update_class, name='update_class'),
    path('delete_class/<int:class_id>/', views.delete_class, name='delete_class'),

    path('sections/', views.section_list, name='section_list'),
    path('add_section/', views.add_section, name='add_section'),
    path('update_section/<int:section_id>/', views.update_section, name='update_section'),
    path('delete_section/<int:section_id>/', views.delete_section, name='delete_section'),

    path('subjects/', views.subject_list, name='subject_list'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('update_subject/<int:subject_id>/', views.update_subject, name='update_subject'),
    path('delete_subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),

    path('class_subjects/', views.class_subject_list, name='class_subject_list'),
    path('add_class_subject/', views.add_class_subject, name='add_class_subject'),
    path('clear_class_subject/<int:section_name_id>/', views.clear_class_subject, name='clear_class_subject'),
]
