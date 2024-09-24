from django.db import models

# Create your models here.

class resume(models.Model):
    full_name = models.CharField(max_length=100)
    birth_date  = models.DateField()
    email = models.EmailField(max_length=100)
    phone_number  = models.CharField(max_length=20)
    professional_summary = models.TextField()

