from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('operator', 'Оператор'),
        ('back_office', 'Бэк-офис'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    def __str__(self):
        return self.username
class Complaint(models.Model):
    STATUS_CHOICES = (
        ('open', 'Открыта'),
        ('in_progress', 'В работе'),
        ('closed', 'Закрыта'),
    )
    client_account = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    client_phone = models.CharField(max_length=20)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(CustomUser, related_name='assigned_complaints', on_delete=models.SET_NULL, null=True)
    comments = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_complaints')
    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     related_name='created_complaints',
    #     on_delete=models.SET_NULL,
    #     null=True
    # )
    # client_account = models.CharField(max_length=100)
    # client_name = models.CharField(max_length=100)
    # client_phone = models.CharField(max_length=15)
    # description = models.TextField()
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    # assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_complaints', limit_choices_to={'role': 'back_office_specialist'}, on_delete=models.SET_NULL, null=True, blank=True)
    # # assigned_to = models.ForeignKey(CustomUser, related_name='assigned_complaints', on_delete=models.SET_NULL, null=True)
    # comments = models.TextField(blank=True, default='')
    def __str__(self):
        return f"Complaint from {self.client_name} ({self.client_account})"