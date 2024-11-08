from django.db import models

class Resume(models.Model):
    customer = models.ForeignKey('access.Customer', on_delete=models.CASCADE, related_name='resumes_manage')  # Cambiamos related_name
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, default='')
    birth_date = models.DateField(default="1900-01-01")
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    professional_summary = models.TextField()
    company_name = models.CharField(max_length=255, default='')
    position = models.CharField(max_length=255, default='')
    start_date = models.DateField(blank=True, null=True, default="1900-01-01")
    end_date = models.DateField(blank=True, null=True, default="1900-01-01")
    description = models.TextField(default='')
    degree = models.CharField(max_length=255, default='')
    institution = models.CharField(max_length=255, default='')
    start_date_education = models.DateField(default="1900-01-01")
    end_date_education = models.DateField(blank=True, null=True, default="1900-01-01")
    description_education = models.TextField(default='')
    skill_name = models.CharField(max_length=255, default='')
    proficiency_level = models.CharField(max_length=255, default='')
    language = models.CharField(max_length=255, default='')
    fluency = models.CharField(max_length=255, default='')
    project_name = models.CharField(max_length=255, default='')
    description_project = models.TextField(default='')
    technologies_used = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255, default='')
    institution_certification = models.CharField(max_length=255, default='')
    date_obtained = models.DateField(blank=True, null=True, default="1900-01-01")
    reference_name = models.CharField(max_length=255, default='')
    relationship = models.CharField(max_length=255, default='')
    contact_info = models.CharField(max_length=255, default='')

class Resume_Uploaded(models.Model):
    customer = models.ForeignKey('access.Customer', on_delete=models.CASCADE, related_name='resumes_uploaded_manage')  # Cambiamos related_name
    content = models.CharField(max_length=10000, null=True)
    file = models.FileField(upload_to='resume/')
