# Generated by Django 5.0.7 on 2024-08-24 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_rename_usuario_resume'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='phone',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
