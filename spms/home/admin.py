from django.contrib import admin
from .models import School, SchoolSession, Class, Section, Subject, SectionSubject, StudentEnrollment

# Registering models to be accessible in the admin panel
admin.site.register(School)
admin.site.register(SchoolSession)
admin.site.register(Class)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(SectionSubject)
admin.site.register(StudentEnrollment)
