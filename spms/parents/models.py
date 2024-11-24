from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Family(models.Model):
    family_id = models.CharField(max_length=100, unique=True)
    guardian = models.ForeignKey('Parent', on_delete=models.CASCADE, related_name='guardians', blank=True, null=True)
    
    def __str__(self):
        return f"Family ID: {self.family_id}"
    
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cnic = models.CharField(max_length=15, unique=True, blank=True, null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{7}-\d{1}$',
                message='CNIC must be in the format 12345-6789012-3',
                code='invalid_cnic'
        )]
    )
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    relationship = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="parents")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.relationship})'