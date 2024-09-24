from django.db import models
from access.models import Customer

# Create your models here.

class Resume(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='resumes')
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    resume_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    professional_summary = models.TextField()
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    #description = models.TextField()
    #end_date = models.DateField()
    #degree = models.CharField(max_length=255)
    #institution = models.CharField(max_length=255)
    #start_date = models.DateField(default=None)
    #end_date = models.DateField(default=None)
    #description = models.TextField(default='')
    #skill_name = models.CharField(max_length=255)
    #proficiency_level = models.CharField(max_length=255)
    #language = models.CharField(max_length=255)
    #fluency = models.CharField(max_length=255)
    #project_name = models.CharField(max_length=255)
    #description = models.TextField(default='')
    #technologies_used = models.CharField(max_length=255)
    #title = models.CharField(max_length=255)
    #institution = models.CharField(max_length=255)
    #date_obtained = models.DateField(default=None)
    #reference_name = models.CharField(max_length=255)
    #relationship = models.CharField(max_length=255)
    #contact_info = models.CharField(max_length=255)