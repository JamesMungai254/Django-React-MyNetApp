from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Student, Note, Assignment, SharedFile, SchoolFee
from .form import ProfilePictureForm

def home(request):
    user = request.user
    student = None
    if hasattr(user, 'student_profile'):
        student = user.student_profile
    return render(request, 'core/home.html',{'student': student})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        secret_key = request.POST['secret_key']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('signup')

        if secret_key == "student_key":
            user = User.objects.create_user(username=username, password=password, is_student=True)
            Student.objects.create(user=user)
            messages.success(request, 'Student account created successfully!')
        elif secret_key == "admin_key":
            user = User.objects.create_user(username=username, password=password, is_admin=True)
            messages.success(request, 'Admin account created successfully!')
        else:
            messages.error(request, 'Invalid secret key!')

        return redirect('login')
    return render(request, 'core/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect('admin_dashboard')
            elif user.is_student:
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'core/login.html')

@login_required
def student_dashboard(request):
    user = request.user
    try:
        student = user.student_profile
    except Student.DoesNotExist:
        messages.error(request, 'Student profile does not exist.')
        return redirect('home')

    notes = Note.objects.filter(student=student)
    shared_files = SharedFile.objects.filter(student=student)
    assignments = Assignment.objects.filter(student=student)

    try:
        fees = SchoolFee.objects.filter(student=student).first()
    except SchoolFee.DoesNotExist:
        fees = None

    if request.method == 'POST':
        if 'create_note' in request.POST:
            title = request.POST.get('title')
            content = request.POST.get('content')
            Note.objects.create(student=student, title=title, content=content)
            messages.success(request, 'Note created successfully!')
            return redirect('student_dashboard')
        elif 'delete_note' in request.POST:
            note_id = request.POST.get('note_id')
            note = get_object_or_404(Note, id=note_id, student=student)
            note.delete()
            messages.success(request, 'Note deleted successfully!')
            return redirect('student_dashboard')
        elif 'upload_picture' in request.POST:
            form = ProfilePictureForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile picture updated successfully.')
            else:
                messages.error(request, 'Error updating profile picture.')
    
    form = ProfilePictureForm(instance=student)
    
    return render(request, 'core/student_dashboard.html', {
        'notes': notes,
        'fees': fees,
        'shared_files': shared_files,
        'assignments': assignments,
        'form': form,
    })

@login_required
def admin_dashboard(request):
    students = Student.objects.all()
    student_fees = {student.id: student.school_fee for student in students if hasattr(student, 'school_fee')}
    student_notes = {student.id: Note.objects.filter(student=student) for student in students}

    if request.method == 'POST':
        if 'delete_student' in request.POST:
            student_id = request.POST['student_id']
            Student.objects.filter(id=student_id).delete()
            messages.success(request, 'Student deleted successfully.')
        elif 'set_fee' in request.POST:
            student_id = request.POST['student_id']
            total_fee = request.POST['total_fee']
            fee_paid = request.POST['fee_paid']
            student = Student.objects.get(id=student_id)
            school_fee, created = SchoolFee.objects.get_or_create(student=student)
            school_fee.total_fee = total_fee
            school_fee.fee_paid = fee_paid
            school_fee.save()
            messages.success(request, 'Student fees updated successfully.')
        elif 'share_file' in request.POST:
            student_id = request.POST['student_id']
            file = request.FILES['file']
            description = request.POST['description']
            student = Student.objects.get(id=student_id)
            SharedFile.objects.create(student=student, file=file, description=description)
            messages.success(request, 'File shared successfully.')
        elif 'assign_task' in request.POST:
            student_id = request.POST['student_id']
            title = request.POST['title']
            description = request.POST['description']
            student = Student.objects.get(id=student_id)
            Assignment.objects.create(student=student, title=title, description=description)
            messages.success(request, 'Assignment created successfully.')
        elif 'approve_assignment' in request.POST:
            assignment_id = request.POST['assignment_id']
            assignment = Assignment.objects.get(id=assignment_id)
            assignment.is_completed = True
            assignment.save()
            messages.success(request, 'Assignment approved.')
        elif 'reject_assignment' in request.POST:
            assignment_id = request.POST['assignment_id']
            assignment = Assignment.objects.get(id=assignment_id)
            assignment.is_completed = False
            assignment.save()
            messages.success(request, 'Assignment rejected.')

    return render(request, 'core/admin_dashboard.html', {
        'students': students,
        'student_fees': student_fees,
        'student_notes': student_notes,
        'assignments': Assignment.objects.all(),
        'shared_files': SharedFile.objects.all(),
    })


def logout_view(request):
    logout(request)
    return redirect('home')
