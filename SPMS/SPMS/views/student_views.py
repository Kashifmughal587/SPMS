from django.shortcuts import render

def dashboard(request):
    return render(request, 'school/student/dashboard.html')

def student_login(request):
    return render(request, 'school/student/login.html')