# Generated by Django 5.0.7 on 2024-09-23 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes_manage', '0003_rename_email_resume_resume_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certification',
            name='resume',
        ),
        migrations.RemoveField(
            model_name='education',
            name='resume',
        ),
        migrations.RemoveField(
            model_name='language',
            name='resume',
        ),
        migrations.RemoveField(
            model_name='project',
            name='resume',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='resume',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='resume',
        ),
        migrations.RemoveField(
            model_name='workexperience',
            name='resume',
        ),
        migrations.AddField(
            model_name='resume',
            name='certifications',
            field=models.ManyToManyField(to='resumes_manage.certification'),
        ),
        migrations.AddField(
            model_name='resume',
            name='educations',
            field=models.ManyToManyField(to='resumes_manage.education'),
        ),
        migrations.AddField(
            model_name='resume',
            name='languages',
            field=models.ManyToManyField(to='resumes_manage.language'),
        ),
        migrations.AddField(
            model_name='resume',
            name='projects',
            field=models.ManyToManyField(to='resumes_manage.project'),
        ),
        migrations.AddField(
            model_name='resume',
            name='references',
            field=models.ManyToManyField(to='resumes_manage.reference'),
        ),
        migrations.AddField(
            model_name='resume',
            name='skills',
            field=models.ManyToManyField(to='resumes_manage.skill'),
        ),
        migrations.AddField(
            model_name='resume',
            name='work_experiences',
            field=models.ManyToManyField(to='resumes_manage.workexperience'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='date_obtained',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='certification',
            name='institution',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='certification',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='education',
            name='degree',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='education',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='education',
            name='end_date',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='education',
            name='institution',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='education',
            name='start_date',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='language',
            name='fluency',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='language',
            name='language',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='reference',
            name='reference_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='reference',
            name='relationship',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='resume',
            name='full_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='resume',
            name='resume_email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='skill',
            name='proficiency_level',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='skill',
            name='skill_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='company_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='position',
            field=models.CharField(max_length=255),
        ),
    ]
