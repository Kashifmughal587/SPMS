from django import forms
from home.models import SchoolSession, Class, Section, Subject, ClassSubject

class SchoolSessionForm(forms.ModelForm):
    class Meta:
        model = SchoolSession
        fields = ['school', 'start_date', 'end_date', 'current']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'description', 'session']
        
class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['class_name', 'name', 'description']
        
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']
        
class ClassSubjectForm(forms.ModelForm):
    class Meta:
        model = ClassSubject
        fields = ['class_name', 'subject']