from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from students.models import Student
from django.contrib import messages

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
    students = Student.objects.select_related(
        'family', 
        'family__guardian_id', 
        'family__guardian_id__user'
    ).values(
        'id', 
        'registration_number', 
        'user__first_name', 
        'user__last_name',
        'family__family_id', 
        'family__guardian_id__user__first_name', 
        'family__guardian_id__user__last_name',
        'gender'
    )

    user = request.user
    return render(request, 'students.html', {
        'page': 'Students',
        'user' : user,
        'student_list': students,
        'user': request.user
    })
    
def add_student(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Student added successfully!')
#             return redirect('studentlist')
#         else:
#             messages.error(request, 'There was an error adding the student. Please check the form.')
#     else:
#         form = StudentForm()
    last_student = Student.objects.order_by('-id').first()

    if last_student:
        # Extract the numeric part from the last registration number
        last_registration_number = int(last_student.registration_number.replace("REG", ""))
        new_registration_number = f"REG{last_registration_number + 1:04d}"  # Increment and format
    else:
        # If there are no students yet, start with REG0001
        new_registration_number = "REG0001"
        
    return render(request, 'add_student.html', {
        'reg_no' : new_registration_number
    })
    
def student_detail(request, student_id):
    return (request)
