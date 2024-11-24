from django.contrib import admin
from .models import School, SchoolSession, Class, Section, Subject, ClassSubject, StudentEnrollment

# Registering models to be accessible in the admin panel
admin.site.register(School)
admin.site.register(SchoolSession)
admin.site.register(Class)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(ClassSubject)
admin.site.register(StudentEnrollment)
