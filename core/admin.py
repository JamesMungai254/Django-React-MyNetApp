from django.contrib import admin

# Register your models here.
# core/admin.py

from .models import User, Student, Note, Assignment, SharedFile, SchoolFee
'''
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Note)
admin.site.register(Assignment)
admin.site.register(SharedFile)
admin.site.register(SchoolFee)
'''


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    pass

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    pass

@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    pass

@admin.register(SchoolFee)
class SchoolFeeAdmin(admin.ModelAdmin):
    pass

