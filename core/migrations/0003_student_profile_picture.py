# Generated by Django 4.2.15 on 2024-08-13 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_assignment_student_alter_note_student_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
