from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    passport_series = models.CharField(
    max_length=9,
    unique=True,
    null=True,  
    verbose_name='Серия паспорта'
)


    def __str__(self):
        return f"{self.username} ({self.passport_series})"
