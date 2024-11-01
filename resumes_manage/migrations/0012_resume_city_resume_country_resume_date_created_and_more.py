# Generated by Django 5.0.7 on 2024-10-30 19:32

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes_manage', '0011_alter_resume_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='city',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='resume',
            name='country',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='resume',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resume',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='expected_salary',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='resume',
            name='gender',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='resume',
            name='id_card',
            field=models.CharField(default='', max_length=255),
        ),
    ]
