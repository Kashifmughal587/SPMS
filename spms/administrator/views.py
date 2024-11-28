from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from home.models import Class, Section, Subject, SectionSubject, SchoolSession
from students.models import Student
from parents.models import Family, Parent
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse

#########################################################################################################
#                                               DASHBOARD                                               #
#########################################################################################################

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
    
#########################################################################################################
#                                       STUDENT END POINTS                                              #
#########################################################################################################

@login_required
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
    return render(request, 'list_students.html', {
        'page': 'Students',
        'user' : user,
        'student_list': students,
        'user': request.user
    })

@login_required
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
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
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
                'first_name': request.POST.get('father_first_name').strip(),
                'last_name': request.POST.get('father_last_name').strip(),
                'cnic': request.POST.get('father_cnic'),
                'email': request.POST.get('father_email'),
                'phone_number': request.POST.get('father_mobile'),
                'whatsapp': request.POST.get('father_whatsapp'),
                'education': request.POST.get('father_education'),
                'profession': request.POST.get('father_profession'),
                'relationship': 'Father',
            },
            'mother': {
                'first_name': request.POST.get('mother_first_name').strip(),
                'last_name': request.POST.get('mother_last_name').strip(),
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
        last_student = Student.objects.order_by('-id').first()
        new_registration_number = f"REG{(int(last_student.registration_number[3:]) + 1) if last_student else 1:04d}"
        user = request.user
        return render(request, 'add_student.html', {
            'page': 'Students',
            'user' : user,
            'reg_no': new_registration_number
            })

@login_required
def student_detail(request, student_id):
    return (request)

#########################################################################################################
#                                       SESSION END POINTS                                              #
#########################################################################################################

# def school_session_list(request):
#     sessions = SchoolSession.objects.all()
#     return render(request, 'school_session_list.html', {'sessions': sessions})

# def add_school_session(request):
#     if request.method == 'POST':
#         form = SchoolSessionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('school_session_list')
#     else:
#         form = SchoolSessionForm()
#     return render(request, 'add_school_session.html', {'form': form})

# def update_school_session(request, pk):
#     session = SchoolSession.objects.get(pk=pk)
#     if request.method == 'POST':
#         form = SchoolSessionForm(request.POST, instance=session)
#         if form.is_valid():
#             form.save()
#             return redirect('school_session_list')
#     else:
#         form = SchoolSessionForm(instance=session)
#     return render(request, 'update_school_session.html', {'form': form})

# def delete_school_session(request, pk):
#     session = SchoolSession.objects.get(pk=pk)
#     session.delete()
#     return redirect('school_session_list')

#########################################################################################################
#                                       CLASS END POINTS                                                #
#########################################################################################################

# Read
@login_required
def class_list(request):
    classes = Class.objects.all()
    user = request.user
    return render(request, 'list_classes.html', {
        'page': 'Class',
        'user' : user,
        'classes': classes
        })

# Create
@login_required
def add_class(request):
    if request.method == "POST":
        required_fields = ['class_name']
        user = request.user
        missing_fields = [field for field in required_fields if not request.POST.get(field)]
        if missing_fields:
            messages.error(request, f"Please fill in required fields: {', '.join(missing_fields)}.")
            return render(request, 'add_update_class.html', {
                'page': 'Class',
                'user' : user,
                })
        
        current_session = SchoolSession.objects.filter(current=True).first()
        if not current_session:
            messages.error(request, "No current school session is active. Please set one before adding a class.")
            return render(request, 'add_update_class.html', {
                'page': 'Class',
                'user' : user,
                })
            
        class_name = request.POST.get('class_name').strip()
        class_description = request.POST.get('class_description')
        
        if Class.objects.filter(name__iexact=class_name).exists():
            messages.error(request, f"A Class with the name '{class_name}' already exists!")
            return render(request, 'add_update_class.html', {
                'page': 'Class',
                'user' : user,
                })

        new_class = Class.objects.create(
            name=class_name,
            description=class_description,
            session=current_session,
        )

        messages.success(request, f"Class '{new_class.name}' has been added successfully!")
        return redirect('class_list')
    else:
        user = request.user
        return render(request, 'add_update_class.html', {
            'page': 'Class',
            'user' : user
            })

# Update
@login_required
def update_class(request, class_id):
    class_obj = get_object_or_404(Class, pk=class_id)
    user = request.user

    if request.method == "POST":
        required_fields = ['class_name']
        missing_fields = [field for field in required_fields if not request.POST.get(field)]
        if missing_fields:
            messages.error(request, f"Please fill in required fields: {', '.join(missing_fields)}.")
            return render(request, 'add_update_class.html', {
                'page': 'Class',
                'user': user,
                'class_obj': class_obj,
            })

        class_name = request.POST.get('class_name').strip()
        class_description = request.POST.get('class_description')
        
        if Class.objects.filter(name__iexact=class_name).exclude(pk=class_obj.pk).exists():
            messages.error(request, f"A Class with the name '{class_name}' already exists!")
            return render(request, 'add_update_class.html', {
                'page': 'Class',
                'user': user,
                'class_obj': class_obj,
            })

        class_obj.name = class_name
        class_obj.description = class_description
        class_obj.save()

        messages.success(request, f"Class '{class_obj.name}' has been updated successfully!")
        return redirect('class_list')

    return render(request, 'add_update_class.html', {
        'page': 'Class',
        'user': user,
        'class_obj': class_obj,
    })

# Delete
@login_required
def delete_class(request, class_id):
    class_obj = get_object_or_404(Class, pk=class_id)
    class_obj.delete()
    messages.success(request, f"Subject '{class_obj.name}' has been deleted successfully!")
    return redirect('class_list')

#########################################################################################################
#                                       SECTION END POINTS                                              #
#########################################################################################################

# Read
@login_required
def section_list(request):
    sections = Section.objects.all()
    user = request.user
    return render(request, 'list_sections.html', {
        'page': 'Section',
        'user' : user,
        'sections': sections
        })
    
# Create
@login_required
def add_section(request):
    user = request.user
    if request.method == "POST":
        required_fields = ['section_name', 'class_id']
        missing_fields = [field for field in required_fields if not request.POST.get(field)]
        if missing_fields:
            messages.error(request, f"Please fill in required fields: {', '.join(missing_fields)}.")
            classes = Class.objects.all()
            return render(request, 'add_update_section.html', {
                'page': 'Section',
                'user' : user,
                'classes' : classes
                })

        section_name = request.POST.get('section_name').strip()
        section_description = request.POST.get('section_description')
        class_id = request.POST.get('class_id')
        class_obj = get_object_or_404(Class, pk=class_id)

        if Section.objects.filter(name__iexact=section_name, class_name=class_obj).exists():
            messages.error(request, f"A section with the name '{section_name}' already exists in class '{class_obj.name}'.")
            classes = Class.objects.all()
            return render(request, 'add_update_section.html', {
                'page': 'Section',
                'user': user,
                'classes': classes
            })

        new_section = Section.objects.create(
            class_name=class_obj,
            name=section_name,
            description=section_description,
        )
        messages.success(request, f"Section '{new_section.name}' has been added successfully!")
        return redirect('section_list')
    else:
        classes = Class.objects.all()
    return render(request, 'add_update_section.html', {
        'page': 'Section',
        'user' : user,
        'classes' : classes
        })

# Update
@login_required
def update_section(request, section_id):
    section_obj = get_object_or_404(Section, pk=section_id)
    user = request.user
    if request.method == "POST":
        required_fields = ['section_name', 'class_id']
        missing_fields = [field for field in required_fields if not request.POST.get(field)]
        if missing_fields:
            messages.error(request, f"Please fill in required fields: {', '.join(missing_fields)}.")
            classes = Class.objects.all()
            return render(request, 'add_update_section.html', {
                'page': 'Section',
                'user' : user,
                'classes' : classes
                })

        section_name = request.POST.get('section_name').strip()
        section_description = request.POST.get('section_description')
        class_id = request.POST.get('class_id')
        class_obj = get_object_or_404(Class, pk=class_id)

        if Section.objects.filter(name__iexact=section_name, class_name=class_obj).exclude(pk=section_obj.pk).exists():
            messages.error(request, f"A section with the name '{section_name}' already exists in class '{class_obj.name}'.")
            classes = Class.objects.all()
            return render(request, 'add_update_section.html', {
                'page': 'Section',
                'user': user,
                'classes': classes,
                'section_obj': section_obj
            })
        
        section_obj.name = section_name
        section_obj.description = section_description
        section_obj.class_name = class_obj
        section_obj.save()
        return redirect('section_list')
    else:
        classes = Class.objects.all()
    return render(request, 'add_update_section.html', {
        'page': 'Section',
        'user' : user,
        'classes' : classes,
        'section_obj' : section_obj
        })

# Delete
@login_required
def delete_section(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    section.delete()
    messages.success(request, f"Subject '{section.name}' has been deleted successfully!")
    return redirect('section_list')

#########################################################################################################
#                                       SUBJECT END POINTS                                              #
#########################################################################################################

# Read
@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    user = request.user
    return render(request, 'list_subjects.html', {
        'page': 'Subject',
        'user' : user,
        'subjects': subjects})
    
# Create
@login_required
def add_subject(request):
    user = request.user
    if request.method == "POST":
        required_fields = ['subject_name']
        user = request.user
        missing_fields = [field for field in required_fields if not request.POST.get(field)]
        if missing_fields:
            messages.error(request, f"Please fill in required fields: {', '.join(missing_fields)}.")
            return render(request, 'add_update_subject.html', {
                'page': 'Subject',
                'user' : user,
                })
            
        subject_name = request.POST.get('subject_name').strip()
        subject_description = request.POST.get('subject_description')
        
        if Subject.objects.filter(name__iexact=subject_name).exists():
            messages.error(request, f"A Subject with the name '{subject_name}' already exists!")
            return render(request, 'add_update_subject.html', {
                'page': 'Subject',
                'user' : user,
                })

        new_subject = Subject.objects.create(
            name=subject_name,
            description=subject_description,
        )

        messages.success(request, f"Subject '{new_subject.name}' has been added successfully!")
        return redirect('subject_list')
    else:
        user = request.user
        return render(request, 'add_update_subject.html', {
            'page': 'Subject',
            'user' : user})


# Update
@login_required
def update_subject(request, subject_id):
    subject_obj = get_object_or_404(Subject, pk=subject_id)
    user = request.user

    if request.method == "POST":
        required_fields = ['subject_name']
        missing_fields = [field for field in required_fields if not request.POST.get(field)]
        if missing_fields:
            messages.error(request, f"Please fill in required fields: {', '.join(missing_fields)}.")
            return render(request, 'add_update_subject.html', {
                'page': 'Subject',
                'user': user,
                'subject_obj': subject_obj,
            })

        subject_name = request.POST.get('subject_name').strip()
        subject_description = request.POST.get('subject_description')
        
        if Subject.objects.filter(name__iexact=subject_name).exclude(pk=subject_obj.pk).exists():
            messages.error(request, f"A Subject with the name '{subject_name}' already exists!")
            subjectes = Subject.objects.all()
            return render(request, 'add_update_subject.html', {
                'page': 'Subject',
                'user': user,
                'subject_obj': subject_obj,
            })

        subject_obj.name = subject_name
        subject_obj.description = subject_description
        subject_obj.save()

        messages.success(request, f"Subject '{subject_obj.name}' has been updated successfully!")
        return redirect('subject_list')

    return render(request, 'add_update_subject.html', {
        'page': 'Subject',
        'user': user,
        'subject_obj': subject_obj,
    })

# Delete
@login_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    subject.delete()
    messages.success(request, f"Subject '{subject.name}' has been deleted successfully!")
    return redirect('subject_list')

#########################################################################################################
#                                    CLASS - SUBJECT END POINTS                                         #
#########################################################################################################

# Read
@login_required
def class_subject_list(request):
    classes = Class.objects.all().prefetch_related(
        'sections',
        'sections__section_subjects__subject'
    )
    user = request.user
    return render(request, 'list_class_subject.html', {
        'page': 'Subject',
        'user': user,
        'classes': classes
    })
    
# Create
@login_required
def add_class_subject(request):
    user = request.user
    classes = Class.objects.all().prefetch_related('sections', 'sections__section_subjects__subject')
    available_subjects = Subject.objects.all()
    
    if request.method == "POST":
        required_fields = ['class_id', 'section_id', 'added_subjects']
        user = request.user
        missing_fields = [field for field in required_fields if not request.POST.get(field)]
        if missing_fields:
            messages.error(request, f"Please fill in required fields: {', '.join(missing_fields)}.")
            return render(request, 'add_update_class_subject.html', {
                'page': 'Subject',
                'user': user,
                'available_subjects': available_subjects,
                'classes': classes,
            })
        
        class_id = request.POST.get('class_id')
        section_id = request.POST.get('section_id')
        added_subjects = request.POST.getlist('added_subjects')
        
        section = Section.objects.get(id=section_id, class_name_id=class_id)
        
        existing_subjects = set(section.section_subjects.values_list('subject_id', flat=True))
        new_subjects = set(map(int, added_subjects))
        
        subjects_to_add = new_subjects - existing_subjects
        
        subjects_to_remove = existing_subjects - new_subjects
        
        section.section_subjects.filter(subject_id__in=subjects_to_remove).delete()
        
        for subject_id in subjects_to_add:
            subject = Subject.objects.get(id=subject_id)
            section.section_subjects.create(subject=subject)
        
        messages.success(request, "Subjects successfully updated for the section.")
        return redirect('class_subject_list')
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        class_id = request.GET.get('class_id')
        section_id = request.GET.get('section_id')

        if section_id:
            added_subjects = SectionSubject.objects.filter(section_name_id=section_id).select_related('subject')
            added_subjects_data = [{"id": subject.subject.id, "name": subject.subject.name} for subject in added_subjects]

            return JsonResponse({
                'added_subjects': added_subjects_data
            })
        
        if class_id:
            sections = Section.objects.filter(class_name_id=class_id)
            sections_data = [{"id": section.id, "name": section.name} for section in sections]
            return JsonResponse({
                'sections': sections_data
            })
    
    return render(request, 'add_update_class_subject.html', {
        'page': 'Subject',
        'user': user,
        'available_subjects' : available_subjects,
        'classes': classes,
    })

# Clear All Subjects
@login_required
def clear_class_subject(request, section_name_id):
    section_subjects = SectionSubject.objects.filter(section_name_id=section_name_id)
    section_subjects.delete()
    return redirect('class_subject_list')
