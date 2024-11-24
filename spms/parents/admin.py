from django.contrib import admin
from .models import Parent, Family

# Registering models to be accessible in the admin panel
admin.site.register(Parent)
admin.site.register(Family)
