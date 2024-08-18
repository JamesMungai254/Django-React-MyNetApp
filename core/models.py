from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=50)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fees_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Note(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=100)
    content = models.TextField()

class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='assignments')
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class SharedFile(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='shared_files')
    file = models.FileField(upload_to='shared_files/')
    description = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class SchoolFee(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='school_fee')
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    fee_paid = models.DecimalField(max_digits=10, decimal_places=2)
