from django.db import models
from django.contrib.auth.models import User
from parents.models import Family
from django.utils import timezone
from django.core.validators import RegexValidator

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=100, unique=True, editable=False)
    cnic = models.CharField(max_length=15, unique=True, blank=True, null=True,
        validators=[RegexValidator(
            regex=r'^\d{5}-\d{7}-\d{1}$',
            message='CNIC must be in the format 12345-6789012-3',
            code='invalid_cnic'
        )]
    )
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="students")
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    religion = models.CharField(max_length=50, blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    permanent_city = models.TextField(blank=True, null=True)
    permanent_state = models.TextField(blank=True, null=True)
    permanent_country = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    profile_picture = models.ImageField(upload_to='img/student_pics/', blank=True, null=True)
    admission_date = models.DateField(default=timezone.now)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        if not self.registration_number:
            last_student = Student.objects.order_by('-id').first()
            last_registration_number = int(last_student.registration_number.replace("REG", "")) if last_student else 0
            self.registration_number = f"REG{last_registration_number + 1:04d}"
        super().save(*args, **kwargs)
