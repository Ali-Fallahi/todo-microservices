from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model that inherits from Django's AbstractUser.
    We can add extra fields here in the future.
    """

    # For now, we don't need any extra fields.
    # Example for the future:
    # bio = models.TextField(blank=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    pass
