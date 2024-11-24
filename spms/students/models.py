from django.db import models
from django.contrib.auth.models import User
from parents.models import Parent, Family
from django.utils import timezone

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=100, unique=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="students")
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='img/student_pics/', blank=True, null=True)
    admission_date = models.DateField(default=timezone.now)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
