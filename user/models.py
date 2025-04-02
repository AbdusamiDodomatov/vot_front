from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    is_voter = models.BooleanField(default=True)  
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="user_custom_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="user_custom_permissions")

    def __str__(self):
        return self.username
