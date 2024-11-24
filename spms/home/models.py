from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# School Model
class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    established_year = models.PositiveIntegerField()

    def __str__(self):
        return self.name

# School Session Model (e.g., 2023-2024)
class SchoolSession(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="sessions")
    start_date = models.DateField()
    end_date = models.DateField()
    current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.start_date.year}-{self.end_date.year}"

# Class Model (e.g., Grade 1, Grade 2, etc.)
class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    session = models.ForeignKey(SchoolSession, on_delete=models.CASCADE, related_name="classes")
    
    def __str__(self):
        return f"{self.name} - {self.school.name}"

# Section Model (e.g., A, B, C for each class)
class Section(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=5)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.class_name.name} - Section {self.name}"

# Subject Model (e.g., Mathematics, Science, etc.)
class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Class-Subject Model (Link Subjects to Classes)
class ClassSubject(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="class_subjects")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="class_subjects")
    
    def __str__(self):
        return f"{self.class_name.name} - {self.subject.name}"

# Student Enrollment Model (link students to classes and sections)
class StudentEnrollment(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name="enrollments")
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="enrollments")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="enrollments")
    enrollment_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.student.first_name} - {self.class_name.name} - {self.section.name}"
