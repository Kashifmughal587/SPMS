from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.groups.filter(name=role).exists():
                auth_login(request, user)
                
                if role == 'Admin':
                    return redirect('admindashboard')
                elif role == 'Teacher':
                    return redirect('teacherDashboard')
                elif role == 'Student':
                    return redirect('studentDashboard')
                elif role == 'Parent':
                    return redirect('parentDashboard')
            else:
                messages.error(request, f"You are not assigned to the '{role}' group.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')