# Generated by Django 5.1.1 on 2024-09-23 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_remove_custom_user_username'),
        ('resumes_manage', '0004_remove_certification_resume_remove_education_resume_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='certifications',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='educations',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='languages',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='projects',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='references',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='skills',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='work_experiences',
        ),
        migrations.AddField(
            model_name='resume',
            name='customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to='access.customer'),
        ),
        migrations.DeleteModel(
            name='Certification',
        ),
        migrations.DeleteModel(
            name='Education',
        ),
        migrations.DeleteModel(
            name='Language',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='Reference',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
        migrations.DeleteModel(
            name='WorkExperience',
        ),
    ]
