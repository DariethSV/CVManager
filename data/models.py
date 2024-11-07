# data/models.py
from django.db import models
from access.models import Custom_User, Customer

class Resume(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=255)
    content = models.TextField()

class Resume_Uploaded(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='uploaded_resumes')
    file = models.FileField(upload_to='uploads/')
    content = models.TextField()
