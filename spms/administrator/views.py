from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from home.models import Class, Section, Subject, ClassSubject, SchoolSession
from students.models import Student
from parents.models import Family, Parent
from django.contrib import messages
from django.utils import timezone
from .forms import ClassSubjectForm, ClassForm, SectionForm, SubjectForm, ClassSubjectForm, SchoolSessionForm

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
    if request.method == 'POST':
        required_fields = ['roll_number', 'birth_certificate', 'first_name', 'last_name', 'dob', 
                           'gender', 'religion', 'emergency_contact', 'address', 'city', 'state', 'country']
        
        missing_fields = [field for field in required_fields if not request.POST.get(field)]
        if missing_fields:
            messages.error(request, f"Please fill in all required fields: {', '.join(missing_fields)}.")
            return render(request, 'add_student.html', {'reg_no': request.POST.get('registration_number')})
        
        # Extracting and assigning fields
        registration_number = request.POST.get('registration_number')
        roll_number = request.POST.get('roll_number')
        birth_certificate = request.POST.get('birth_certificate')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        religion = request.POST.get('religion')
        blood_group = request.POST.get('blood_group', None)
        contact_number = request.POST.get('contact_number', None)
        emergency_contact = request.POST.get('emergency_contact')
        profile_picture = request.FILES.get('profile_picture', None)
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        admission_date = request.POST.get('admission_date', timezone.now())
        same_as_current = request.POST.get('same_as_present') == 'on'
        
        permanent_address = address if same_as_current else request.POST.get('permanent_address', None)
        permanent_city = city if same_as_current else request.POST.get('permanent_city', None)
        permanent_state = state if same_as_current else request.POST.get('permanent_state', None)
        permanent_country = country if same_as_current else request.POST.get('permanent_country', None)
        
        guardian = request.POST.get('guardian', None)

        # Guardian details
        guardian_data = {
            'father': {
                'first_name': request.POST.get('father_first_name'),
                'last_name': request.POST.get('father_last_name'),
                'cnic': request.POST.get('father_cnic'),
                'email': request.POST.get('father_email'),
                'phone_number': request.POST.get('father_mobile'),
                'whatsapp': request.POST.get('father_whatsapp'),
                'education': request.POST.get('father_education'),
                'profession': request.POST.get('father_profession'),
                'relationship': 'Father',
            },
            'mother': {
                'first_name': request.POST.get('mother_first_name'),
                'last_name': request.POST.get('mother_last_name'),
                'cnic': request.POST.get('mother_cnic'),
                'email': request.POST.get('mother_email'),
                'phone_number': request.POST.get('mother_mobile'),
                'whatsapp': request.POST.get('mother_whatsapp'),
                'education': request.POST.get('mother_education'),
                'profession': request.POST.get('mother_profession'),
                'relationship': 'Mother',
            },
        }

        # Create Student User
        username = birth_certificate
        password = f"password{username[-4:]}"
        if User.objects.filter(username=username).exists():
            messages.error(request, "This student already exists.")
            return render(request, 'add_student.html', {'reg_no': registration_number})

        student_user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)

        # Create or retrieve Family
        last_family = Family.objects.order_by('-id').first()
        new_family_id = f"FAM{(int(last_family.family_id[3:]) + 1) if last_family else 1:04d}"
        family, _ = Family.objects.get_or_create(family_id=new_family_id)

        # Save Student
        student = Student.objects.create(
            user=student_user,
            registration_number=registration_number,
            cnic=birth_certificate,
            family=family,
            dob=dob,
            gender=gender,
            religion=religion,
            blood_group=blood_group,
            address=address,
            city=city,
            state=state,
            country=country,
            permanent_address=permanent_address,
            permanent_city=permanent_city,
            permanent_state=permanent_state,
            permanent_country=permanent_country,
            phone_number=contact_number,
            roll_number=roll_number,
            profile_picture=profile_picture,
            admission_date=admission_date,
            emergency_contact=emergency_contact,
        )

        # Add Guardian Information
        for relation, data in guardian_data.items():
            if data['cnic']:
                guardian_username = data['cnic']
                guardian_password = f"password{guardian_username[-4:]}"
                if User.objects.filter(username=guardian_username).exists():
                    messages.error(request, f"{data['relationship']} CNIC already exists.")
                    return render(request, 'add_student.html', {'reg_no': registration_number})
                
                guardian_user = User.objects.create_user(username=guardian_username, email=data['email'], 
                                                         password=guardian_password, first_name=data['first_name'], 
                                                         last_name=data['last_name'])
                Parent.objects.create(
                    user=guardian_user,
                    cnic=data['cnic'],
                    phone_number=data['phone_number'],
                    whatsapp_number=data['whatsapp'],
                    education=data['education'],
                    profession=data['profession'],
                    relationship=data['relationship'],
                    address=permanent_address,
                    family=family,
                )
        
        family.guardian = guardian
        family.save()

        messages.success(request, 'Student added successfully!')
        return redirect('studentlist')
    else:
        # Generate a new registration number
        last_student = Student.objects.order_by('-id').first()
        new_registration_number = f"REG{(int(last_student.registration_number[3:]) + 1) if last_student else 1:04d}"
        return render(request, 'add_student.html', {'reg_no': new_registration_number})
    
def student_detail(request, student_id):
    return (request)

def school_session_list(request):
    sessions = SchoolSession.objects.all()
    return render(request, 'school_session_list.html', {'sessions': sessions})

def add_school_session(request):
    if request.method == 'POST':
        form = SchoolSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('school_session_list')
    else:
        form = SchoolSessionForm()
    return render(request, 'add_school_session.html', {'form': form})

def update_school_session(request, pk):
    session = SchoolSession.objects.get(pk=pk)
    if request.method == 'POST':
        form = SchoolSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('school_session_list')
    else:
        form = SchoolSessionForm(instance=session)
    return render(request, 'update_school_session.html', {'form': form})

def delete_school_session(request, pk):
    session = SchoolSession.objects.get(pk=pk)
    session.delete()
    return redirect('school_session_list')

# Create
def add_class(request):
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm()
    user = request.user
    return render(request, 'add_class.html', {
        'page': 'Class',
        'user' : user,
        'form': form
        })

# Read
def class_list(request):
    classes = Class.objects.all()
    user = request.user
    return render(request, 'class_list.html', {
        'page': 'Class',
        'user' : user,
        'classes': classes
        })

# Update
def update_class(request, class_id):
    class_obj = get_object_or_404(Class, pk=class_id)
    if request.method == "POST":
        form = ClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm(instance=class_obj)
    return render(request, 'update_class.html', {'form': form})

# Delete
def delete_class(request, class_id):
    class_obj = get_object_or_404(Class, pk=class_id)
    if request.method == "POST":
        class_obj.delete()
        return redirect('class_list')
    return render(request, 'delete_class.html', {'class_obj': class_obj})

# Create
def add_section(request):
    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('section_list')
    else:
        form = SectionForm()
    return render(request, 'add_section.html', {'form': form})

# Read
def section_list(request):
    sections = Section.objects.all()
    user = request.user
    return render(request, 'section_list.html', {
        'page': 'Section',
        'user' : user,
        'sections': sections})

# Update
def update_section(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    if request.method == "POST":
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect('section_list')
    else:
        form = SectionForm(instance=section)
    return render(request, 'update_section.html', {'form': form})

# Delete
def delete_section(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    if request.method == "POST":
        section.delete()
        return redirect('section_list')
    return render(request, 'delete_section.html', {'section': section})

# Create
def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'add_subject.html', {'form': form})

# Read
def subject_list(request):
    subjects = Subject.objects.all()
    user = request.user
    return render(request, 'subject_list.html', {
        'page': 'Subject',
        'user' : user,
        'subjects': subjects})

# Update
def update_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'update_subject.html', {'form': form})

# Delete
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == "POST":
        subject.delete()
        return redirect('subject_list')
    return render(request, 'delete_subject.html', {'subject': subject})

# Create
def add_class_subject(request):
    if request.method == "POST":
        form = ClassSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_subject_list')
    else:
        form = ClassSubjectForm()
    return render(request, 'add_class_subject.html', {'form': form})

# Read
def class_subject_list(request):
    class_subjects = ClassSubject.objects.all()
    return render(request, 'class_subject_list.html', {'class_subjects': class_subjects})

# Update
def update_class_subject(request, class_subject_id):
    class_subject = get_object_or_404(ClassSubject, pk=class_subject_id)
    if request.method == "POST":
        form = ClassSubjectForm(request.POST, instance=class_subject)
        if form.is_valid():
            form.save()
            return redirect('class_subject_list')
    else:
        form = ClassSubjectForm(instance=class_subject)
    return render(request, 'update_class_subject.html', {'form': form})

# Delete
def delete_class_subject(request, class_subject_id):
    class_subject = get_object_or_404(ClassSubject, pk=class_subject_id)
    if request.method == "POST":
        class_subject.delete()
        return redirect('class_subject_list')
    return render(request, 'delete_class_subject.html', {'class_subject': class_subject})
