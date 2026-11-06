from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'client', 'client'
        COACH = 'coach', 'coach'
        ADMIN = 'admin', 'admin'

    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.role})'