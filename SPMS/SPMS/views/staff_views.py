from django.shortcuts import render

def dashboard(request):
    return render(request, 'school/staff/dashboard.html')

def staff_login(request):
    return render(request, 'school/staff/login.html')