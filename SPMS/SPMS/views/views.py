from django.shortcuts import render

def home(request):
    return render(request, 'school/home/home.html')

def login(request):
    return render(request, 'school/home/login.html')

def login_process(request):
    return render(request, 'school/admin/dashboard.html')

def logout(request):
    return render (request, 'school/home/home.html')