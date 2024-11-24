from django.contrib.auth.models import User
from django.shortcuts import render

def dashboard(request):
    students_count = User.objects.filter(groups__name='Student').count()
    teachers_count = User.objects.filter(groups__name='Teacher').count()
    parents_count = User.objects.filter(groups__name='Parent').count()
    
    user = request.user
    
    return render(request, 'dashboard.html', {
        'students_count': students_count,
        'teachers_count': teachers_count,
        'parents_count': parents_count,
        'user' : user
    })