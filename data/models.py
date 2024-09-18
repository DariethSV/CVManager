from django.db import models
from access.models import Customer

class Resume(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='resumes',default=None)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, null=True)


    def __str__(self):
        return self.name
