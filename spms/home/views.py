from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = authenticate(request, username=username, password=password)

        if user.groups.filter(name=role).exists():
            auth_login(request, user)
            if role == 'admin':
                return redirect('adminDashboard')
            elif role == 'teacher':
                return redirect('teacherDashboard')
            elif role == 'student':
                return redirect('studentDashboard')
            elif role == 'parent':
                return redirect('parentDashboard')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'login.html')

def logout(request):
    return redirect('home')