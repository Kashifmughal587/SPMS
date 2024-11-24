from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model for authentication
#     guardian = models.ForeignKey(Guardian, on_delete=models.SET_NULL, null=True, related_name="students")
#     dob = models.DateField()  # Date of birth
#     gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
#     address = models.TextField(blank=True, null=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     profile_picture = models.ImageField(upload_to='student_pics/', blank=True, null=True)
#     admission_date = models.DateField(default=timezone.now)  # Admission date
#     class_level = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True)  # Link to the class
#     emergency_contact = models.CharField(max_length=15, blank=True, null=True)  # Emergency contact number

#     def __str__(self):
#         return f'{self.user.first_name} {self.user.last_name}'