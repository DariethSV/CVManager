# Generated by Django 5.0.7 on 2024-11-08 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes_manage', '0019_applied_pages'),
    ]

    operations = [
        migrations.AddField(
            model_name='applied_pages',
            name='user_email',
            field=models.CharField(default='', max_length=255),
        ),
    ]
