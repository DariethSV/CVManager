from django.db import models

# Create your models here.

class Resume(models.Model):
    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    professional_summary = models.TextField()

    def __str__(self):
        return self.full_name

class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='work_experiences')
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)
    proficiency_level = models.CharField(max_length=50)

class Language(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='languages')
    language = models.CharField(max_length=50)
    fluency = models.CharField(max_length=50)

class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    technologies_used = models.CharField(max_length=255)

class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    date_obtained = models.DateField()

class Reference(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='references')
    reference_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)
