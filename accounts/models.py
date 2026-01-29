from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_login_completed = models.BooleanField(default=False)
