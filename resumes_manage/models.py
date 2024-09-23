from django.db import models

# Create your models here.

class Resume(models.Model):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    resume_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    professional_summary = models.TextField()

    work_experiences = models.ManyToManyField('WorkExperience')
    educations = models.ManyToManyField('Education')
    skills = models.ManyToManyField('Skill')
    languages = models.ManyToManyField('Language')
    projects = models.ManyToManyField('Project')
    certifications = models.ManyToManyField('Certification')
    references = models.ManyToManyField('Reference')

class WorkExperience(models.Model):
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

class Education(models.Model):
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None)
    description = models.TextField(default='')

class Skill(models.Model):
    skill_name = models.CharField(max_length=255)
    proficiency_level = models.CharField(max_length=255)

class Language(models.Model):
    language = models.CharField(max_length=255)
    fluency = models.CharField(max_length=255)

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    description = models.TextField(default='')
    technologies_used = models.CharField(max_length=255)

class Certification(models.Model):
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    date_obtained = models.DateField(default=None)

class Reference(models.Model):
    reference_name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)