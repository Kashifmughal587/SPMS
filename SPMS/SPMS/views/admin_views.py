from django.shortcuts import render

def dashboard(request):
    return render(request, 'school/admin/dashboard.html')

def admin_login(request):
    return render(request, 'school/admin/login.html')