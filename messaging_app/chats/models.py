from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add extra fields if you want, e.g.:
    # bio = models.TextField(blank=True, null=True)
    pass
