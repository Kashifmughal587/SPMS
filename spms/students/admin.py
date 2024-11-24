from django.contrib import admin
from .models import Student

# Registering models to be accessible in the admin panel
admin.site.register(Student)
