from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    preferred_theme = models.CharField(max_length=10, default="dark")
    preferred_language = models.CharField(max_length=10, default="en")
