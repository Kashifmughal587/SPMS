from django.db import models
from django.contrib.auth.models import User

class Family(models.Model):
    family_id = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True, null=True)
    guardian = models.ForeignKey('Parent', on_delete=models.CASCADE, related_name="families")

    def __str__(self):
        return f"Family ID: {self.family_id}"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    relationship = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.relationship})'
