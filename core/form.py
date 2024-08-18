from django import forms
from .models import Student

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile_picture']
