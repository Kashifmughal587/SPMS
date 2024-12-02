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

    def save(self, *args, **kwargs):
        if self.current:
            SchoolSession.objects.filter(school=self.school, current=True).update(current=False)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.start_date.year}-{self.end_date.year}"

# Class Model (e.g., Grade 1, Grade 2, etc.)
class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    session = models.ForeignKey(SchoolSession, on_delete=models.CASCADE, related_name="classes")
    
    def __str__(self):
        return f"{self.name}"

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
class SectionSubject(models.Model):
    section_name = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="section_subjects")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="section_subjects")
    
    def __str__(self):
        return f"{self.section_name.name} - {self.subject.name}"

class StudentEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="enrollments")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="enrollments")
    academic_year = models.CharField(max_length=9, blank=True, null=True)  # e.g., "2024-2025"
    roll_number = models.CharField(max_length=20, unique=True, blank=True)
    status = models.CharField(max_length=10, choices=[
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
    ], default='active')
    enrollment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.student.first_name} - {self.roll_number} - {self.academic_year}"
