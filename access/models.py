# access/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from resumes_manage.models import Resume, Resume_Uploaded

class Custom_User_Manager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The user should have an email')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)

class Custom_User(AbstractUser):
    name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    username = None  # Disable the default 'username' field from AbstractUser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = Custom_User_Manager()

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
    )

    class Meta:
        permissions = [
            ("can_view_analytics", "Can view analytics"),
        ]

class Customer(Custom_User):
    resume_used = models.ForeignKey(
        Resume,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='used_by_customer_resume'
    )
    resume_uploaded_used = models.ForeignKey(
        Resume_Uploaded,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='used_by_customer_uploaded'
    )

class Admin_Custom_User(Custom_User):
    class Meta:
        permissions = [
            ("can_view_analytics", "Can view analytics"),
        ]
