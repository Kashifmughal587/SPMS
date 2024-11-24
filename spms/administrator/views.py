from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from students.models import Student

@login_required
def dashboard(request):
    students_count = User.objects.filter(groups__name='Student').count()
    teachers_count = User.objects.filter(groups__name='Teacher').count()
    parents_count = User.objects.filter(groups__name='Parent').count()
    user = request.user
    
    return render(request, 'dashboard.html', {
        'page': 'Dashboard',
        'user' : user,
        'students_count': students_count,
        'teachers_count': teachers_count,
        'parents_count': parents_count,
        
    })
    
def student_list(request):
    students = Student.objects.select_related('family', 'family__guardian', 'family__guardian__user').values(
        'id', 'registration_number', 
        'user__first_name', 'user__last_name',
        'family__family_id', 
        'family__guardian__user__first_name', 
        'family__guardian__user__last_name',
        'gender'
    )

    return render(request, 'students.html', {
        'page': 'Students',
        'student_list': students,
        'user': request.user
    })
    
def student_detail(request, student_id):
    return (request)